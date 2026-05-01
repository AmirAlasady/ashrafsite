#!/usr/bin/env bash
#
# One-shot deploy for the Ashraf Production site on a fresh Ubuntu 24.04 VPS.
#
# Run as a NON-ROOT sudo user (e.g. `ashraf`) AFTER you've cloned this repo.
# Idempotent: safe to re-run after fixing something.
#
# Usage:
#   ./scripts/deploy.sh                              # IP-only deploy, no TLS
#   ./scripts/deploy.sh DOMAIN EMAIL                 # full deploy with TLS
#   ./scripts/deploy.sh ashrafproduction.com a@b.com
#
# After the script finishes:
#   - python manage.py createsuperuser   (interactive — script can't do this)
#   - python manage.py seed_data         (optional, fills demo content)

set -euo pipefail

# --------------------------------------------------------------------------- #
# Config
# --------------------------------------------------------------------------- #
DOMAIN="${1:-}"
EMAIL="${2:-}"
PROJECT_DIR="$HOME/ashrafsite"
REPO_URL="https://github.com/AmirAlasady/ashrafsite.git"
DB_NAME="ashrafsite"
DB_USER="ashraf_app"

step() { echo ""; echo "==> [$1] $2"; }

# --------------------------------------------------------------------------- #
# Sanity checks
# --------------------------------------------------------------------------- #
if [ "$EUID" -eq 0 ]; then
    echo "ERROR: don't run this as root. Run as your sudo user (e.g. 'ashraf')." >&2
    exit 1
fi

if ! sudo -n true 2>/dev/null; then
    echo "This script will use sudo for system-level changes."
    echo "Enter your sudo password if prompted."
    sudo -v
fi

# Keep sudo timestamp fresh in the background so prompts don't appear mid-run
( while true; do sudo -n true; sleep 60; kill -0 $$ 2>/dev/null || exit; done ) &
SUDO_KEEPALIVE_PID=$!
trap 'kill $SUDO_KEEPALIVE_PID 2>/dev/null || true' EXIT

# --------------------------------------------------------------------------- #
# 1 — System update + packages
# --------------------------------------------------------------------------- #
step "1/12" "Updating apt + installing system packages"
sudo apt-get update -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -y -qq
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y -qq \
    python3 python3-venv python3-pip \
    postgresql postgresql-contrib \
    nginx \
    git \
    certbot python3-certbot-nginx \
    fail2ban \
    build-essential libpq-dev \
    curl

# --------------------------------------------------------------------------- #
# 2 — Firewall (UFW)
# --------------------------------------------------------------------------- #
step "2/12" "Configuring UFW (allow SSH + HTTP + HTTPS)"
sudo ufw allow OpenSSH >/dev/null
sudo ufw allow 80/tcp  >/dev/null
sudo ufw allow 443/tcp >/dev/null
sudo ufw --force enable >/dev/null
sudo ufw status

# --------------------------------------------------------------------------- #
# 3 — Postgres database + user
# --------------------------------------------------------------------------- #
step "3/12" "Setting up Postgres database + role"

if sudo -u postgres psql -lqt | cut -d'|' -f1 | grep -qw "$DB_NAME"; then
    echo "    Database '$DB_NAME' already exists; reusing."
    DB_PASSWORD=""    # placeholder; we won't reset the role's password
else
    DB_PASSWORD=$(openssl rand -base64 36 | tr -d '=+/' | cut -c1-40)
    sudo -u postgres psql <<SQL
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\c $DB_NAME
GRANT ALL ON SCHEMA public TO $DB_USER;
SQL
    echo "    Created database '$DB_NAME' and role '$DB_USER'."
fi

# --------------------------------------------------------------------------- #
# 4 — Repo
# --------------------------------------------------------------------------- #
step "4/12" "Cloning or updating the repo"
if [ -d "$PROJECT_DIR/.git" ]; then
    cd "$PROJECT_DIR"
    git pull --ff-only
else
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# --------------------------------------------------------------------------- #
# 5 — Python venv + dependencies
# --------------------------------------------------------------------------- #
step "5/12" "Setting up venv + installing requirements"
if [ ! -d venv ]; then
    python3 -m venv venv
fi
# shellcheck disable=SC1091
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

# --------------------------------------------------------------------------- #
# 6 — .env (only created if missing — preserves existing secrets on re-run)
# --------------------------------------------------------------------------- #
step "6/12" "Writing .env (if not present)"
if [ ! -f .env ]; then
    SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
    PUBLIC_IP=$(curl -s ifconfig.me || echo "127.0.0.1")

    if [ -n "$DOMAIN" ]; then
        ALLOWED_HOSTS="$DOMAIN,www.$DOMAIN,$PUBLIC_IP"
        CSRF_TRUSTED="https://$DOMAIN,https://www.$DOMAIN"
    else
        ALLOWED_HOSTS="$PUBLIC_IP"
        CSRF_TRUSTED=""
    fi

    cat > .env <<EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$ALLOWED_HOSTS
CSRF_TRUSTED_ORIGINS=$CSRF_TRUSTED
DATABASE_URL=postgres://$DB_USER:$DB_PASSWORD@127.0.0.1:5432/$DB_NAME
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
LOG_LEVEL=INFO
EOF
    chmod 600 .env
    echo "    .env created with random SECRET_KEY + DB password."
else
    echo "    .env already exists; not overwriting."
fi

# --------------------------------------------------------------------------- #
# 7 — Migrate + collectstatic + auto-generate logo & favicon from Icon.png
# --------------------------------------------------------------------------- #
step "7/12" "Running migrations and collectstatic"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

step "7b/12" "Generating logo + favicon from Icon.png"
python manage.py shell <<'PYEOF'
from io import BytesIO
from PIL import Image, ImageDraw
from django.core.files.base import ContentFile
from core.models import FooterInfo

footer, _ = FooterInfo.objects.get_or_create(pk=1)

# --- Logo: white background -> transparent
try:
    img = Image.open('Icon.png').convert('RGBA')
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if r >= 235 and g >= 235 and b >= 235:
                pixels[x, y] = (0, 0, 0, 0)
    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    if not footer.logo:
        footer.logo.save('ashraf_logo.png', ContentFile(buf.read()), save=True)
        print(f"  Logo saved: {footer.logo.url}")
    else:
        print("  Logo already set; skipping.")
except FileNotFoundError:
    print("  Icon.png not found; skipping logo generation.")

# --- Favicon: small white circle on transparent
fav = Image.new('RGBA', (256, 256), (0, 0, 0, 0))
ImageDraw.Draw(fav).ellipse((104, 104, 152, 152), fill=(255, 255, 255, 255))
buf = BytesIO()
fav.save(buf, format='PNG', optimize=True)
buf.seek(0)
if not footer.favicon:
    footer.favicon.save('favicon.png', ContentFile(buf.read()), save=True)
    print(f"  Favicon saved: {footer.favicon.url}")
else:
    print("  Favicon already set; skipping.")
PYEOF

# --------------------------------------------------------------------------- #
# 8 — Gunicorn systemd service
# --------------------------------------------------------------------------- #
step "8/12" "Writing gunicorn systemd unit + starting it"
sudo tee /etc/systemd/system/gunicorn.service > /dev/null <<EOF
[Unit]
Description=gunicorn daemon for ashrafsite
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --access-logfile - --error-logfile - --workers 3 --timeout 600 --bind unix:$PROJECT_DIR/gunicorn.sock agency.wsgi:application
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable gunicorn >/dev/null
sudo systemctl restart gunicorn

# nginx (www-data) needs traverse permission on home dir to reach the socket
sudo chmod 755 "$HOME"

# --------------------------------------------------------------------------- #
# 9 — Nginx site (HTTP only first; certbot will add HTTPS block)
# --------------------------------------------------------------------------- #
step "9/12" "Writing nginx site config"
PUBLIC_IP=$(curl -s ifconfig.me || echo "")
if [ -n "$DOMAIN" ]; then
    SERVER_NAME="$DOMAIN www.$DOMAIN $PUBLIC_IP"
else
    SERVER_NAME="${PUBLIC_IP:-_}"
fi

sudo tee /etc/nginx/sites-available/ashrafsite > /dev/null <<EOF
server {
    listen 80;
    server_name $SERVER_NAME;

    client_max_body_size 2G;
    client_body_timeout 600s;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
    }

    location / {
        proxy_set_header Host \$http_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_read_timeout 600s;
        proxy_send_timeout 600s;
        proxy_pass http://unix:$PROJECT_DIR/gunicorn.sock;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/ashrafsite /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# --------------------------------------------------------------------------- #
# 10 — TLS via certbot (only if DOMAIN + EMAIL provided AND DNS resolves)
# --------------------------------------------------------------------------- #
step "10/12" "TLS via certbot"
if [ -n "$DOMAIN" ] && [ -n "$EMAIL" ]; then
    # Check DNS first — saves time on a guaranteed-fail certbot run
    if dig +short "$DOMAIN" | grep -q "$PUBLIC_IP"; then
        sudo certbot --nginx \
            -d "$DOMAIN" -d "www.$DOMAIN" \
            --non-interactive --agree-tos --email "$EMAIL" \
            --redirect || {
                echo "    certbot failed. Re-run manually:"
                echo "      sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN"
            }

        # Flip Django to enforce HTTPS now that the cert is in place
        sed -i 's/^SECURE_SSL_REDIRECT=.*/SECURE_SSL_REDIRECT=True/' .env
        sed -i 's/^SECURE_HSTS_SECONDS=.*/SECURE_HSTS_SECONDS=3600/' .env
        sudo systemctl restart gunicorn
        echo "    .env flipped to enforce HTTPS; gunicorn restarted."
    else
        echo "    DNS for $DOMAIN doesn't point at $PUBLIC_IP yet."
        echo "    Skipping certbot. Once DNS propagates, run:"
        echo "      sudo certbot --nginx -d $DOMAIN -d www.$DOMAIN -m $EMAIL --agree-tos -n --redirect"
    fi
else
    echo "    No DOMAIN/EMAIL; skipping TLS. Site is on http://$PUBLIC_IP/"
fi

# --------------------------------------------------------------------------- #
# 11 — fail2ban (default jail bans IPs after repeated SSH failures)
# --------------------------------------------------------------------------- #
step "11/12" "Enabling fail2ban"
sudo systemctl enable --now fail2ban >/dev/null

# --------------------------------------------------------------------------- #
# 12 — Done
# --------------------------------------------------------------------------- #
step "12/12" "Done"

cat <<EOF

==========================================================
  Deployment complete.
==========================================================

Next steps (interactive — must be done by you):

  cd $PROJECT_DIR
  source venv/bin/activate

  # 1. Create a Django admin login
  python manage.py createsuperuser

  # 2. (Optional) Seed demo content (clients, BTS, projects, team, news)
  python manage.py seed_data

EOF

if [ -n "$DOMAIN" ]; then
    echo "  Site:   https://$DOMAIN/"
    echo "  Admin:  https://$DOMAIN/admin/"
else
    echo "  Site:   http://$PUBLIC_IP/"
    echo "  Admin:  http://$PUBLIC_IP/admin/"
fi
echo ""
