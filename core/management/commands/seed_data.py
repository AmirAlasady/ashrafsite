from io import BytesIO

from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from PIL import Image, ImageDraw

from core.models import (
    AboutInfo,
    BehindTheScenesImage,
    Client,
    FooterInfo,
    HeroSection,
    Post,
)
from contact.models import ContactMessage
from news.models import News, NewsImage
from projects.models import Project, ProjectImage
from team.models import Member


PALETTE = [
    (66, 133, 244),
    (219, 68, 55),
    (244, 180, 0),
    (15, 157, 88),
    (171, 71, 188),
    (255, 112, 67),
    (38, 166, 154),
    (92, 107, 192),
]


def placeholder(label, size=(800, 500), color_index=0):
    """Generate a small solid-color PNG with a label — returns a Django ContentFile."""
    color = PALETTE[color_index % len(PALETTE)]
    img = Image.new("RGB", size, color=color)
    draw = ImageDraw.Draw(img)
    text = label
    bbox = draw.textbbox((0, 0), text)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=(255, 255, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return ContentFile(buf.read(), name=f"{label.lower().replace(' ', '_')}.png")


class Command(BaseCommand):
    help = "Seed the database with fake demo data so the site displays without manual input."

    def add_arguments(self, parser):
        parser.add_argument(
            "--wipe",
            action="store_true",
            help="Delete existing data in all seed-managed models before seeding.",
        )

    def handle(self, *args, **options):
        if options["wipe"]:
            self.stdout.write("Wiping existing demo data...")
            ContactMessage.objects.all().delete()
            Post.objects.all().delete()
            BehindTheScenesImage.objects.all().delete()
            Client.objects.all().delete()
            HeroSection.objects.all().delete()
            FooterInfo.objects.all().delete()
            AboutInfo.objects.all().delete()
            ProjectImage.objects.all().delete()
            Project.objects.all().delete()
            Member.objects.all().delete()
            NewsImage.objects.all().delete()
            News.objects.all().delete()

        self._seed_footer()
        self._seed_hero()
        self._seed_about()
        self._seed_clients()
        self._seed_bts()
        self._seed_posts()
        self._seed_team()
        self._seed_news()
        self._seed_projects()
        self._seed_contact_messages()

        self.stdout.write(self.style.SUCCESS("Seed complete. Visit / to view the site."))

    def _seed_footer(self):
        FooterInfo.objects.get_or_create(
            company_name="Ashraf Studio",
            defaults={
                "tagline": "Marketing & production services that tell better stories.",
                "address": "123 Creative Ave, Cairo, Egypt",
                "email": "hello@ashrafstudio.example",
                "phone": "+20 100 000 0000",
                "instagram": "https://instagram.com/example",
                "facebook": "https://facebook.com/example",
                "twitter": "https://twitter.com/example",
                "linkedin": "https://linkedin.com/company/example",
                "youtube": "https://youtube.com/@example",
                "copyright_text": "© 2026 Ashraf Studio. All rights reserved.",
            },
        )

    def _seed_hero(self):
        if HeroSection.objects.exists():
            return
        hero = HeroSection.objects.create(
            title="We build brands that move people.",
            subtitle="A marketing & production studio for bold ideas.",
            body_text=(
                "From campaign strategy to shooting and post-production, we handle every frame. "
                "Our work has reached audiences in 12 countries and counting."
            ),
            is_active=True,
        )
        hero.background_image.save(
            "hero_bg.png", placeholder("Hero background", size=(1600, 900), color_index=0)
        )

    def _seed_about(self):
        about, created = AboutInfo.objects.get_or_create(
            defaults={
                "who_we_are_title": "Who We Are",
                "who_we_are_body": (
                    "We are a small team of strategists, directors, and editors based in Cairo. "
                    "For six years we've built campaigns for brands that refuse to blend in."
                ),
                "what_we_do_title": "What We Do",
                "what_we_do_body": (
                    "Brand strategy, commercial production, social-first content, and full post-production. "
                    "One team, end to end."
                ),
            }
        )
        if created or not about.background_image:
            about.background_image.save(
                "about_bg.png",
                placeholder("About background", size=(1600, 900), color_index=5),
            )

    def _seed_clients(self):
        clients = [
            ("Nova Foods", "https://example.com/nova"),
            ("Cairo Motors", "https://example.com/cairo-motors"),
            ("Blue Horizon", "https://example.com/bluehorizon"),
            ("Lumen Apparel", "https://example.com/lumen"),
            ("Orbit Telecom", "https://example.com/orbit"),
            ("Harvest Bank", "https://example.com/harvest"),
        ]
        for i, (name, website) in enumerate(clients):
            client, created = Client.objects.get_or_create(
                name=name, defaults={"website": website, "order": i}
            )
            if created:
                client.logo.save(name + ".png", placeholder(name, size=(400, 200), color_index=i))

    def _seed_bts(self):
        if BehindTheScenesImage.objects.exists():
            return
        animations = ["fade-in", "slide-up", "zoom-in", "slide-left", "slide-right", "fade-up"]
        for i in range(6):
            bts = BehindTheScenesImage(
                caption=f"On set — shot {i + 1}",
                animation=animations[i % len(animations)],
                order=i,
            )
            bts.image.save(
                f"bts_{i}.png",
                placeholder(f"BTS {i + 1}", size=(900, 600), color_index=i + 2),
            )
            bts.save()

    def _seed_posts(self):
        samples = [
            ("Summer launch recap", "Three weeks, two cities, one unforgettable shoot."),
            ("Why we shoot on location", "Studios have their place — but real places carry story."),
            ("A note on color grading", "Color isn't decoration. It's emotion on a timeline."),
            ("Our top 5 commercials of the year", "The ones that made the room go quiet."),
        ]
        for i, (name, desc) in enumerate(samples):
            post, created = Post.objects.get_or_create(
                name=name, defaults={"description": desc, "is_published": True}
            )
            if created:
                post.image.save(
                    f"post_{i}.png",
                    placeholder(name[:18], size=(800, 500), color_index=i + 1),
                )

    def _seed_team(self):
        members = [
            ("Ashraf Hassan", "Founder & Creative Director"),
            ("Lina Mostafa", "Head of Production"),
            ("Omar Said", "Senior Editor"),
            ("Yara Fathy", "Brand Strategist"),
            ("Karim Adel", "Director of Photography"),
            ("Nour Ibrahim", "Producer"),
        ]
        for i, (name, role) in enumerate(members):
            member, created = Member.objects.get_or_create(
                name=name,
                defaults={
                    "role": role,
                    "bio": f"{name} leads work across our {role.lower()} practice.",
                    "order": i,
                },
            )
            if created:
                member.image.save(
                    f"member_{i}.png",
                    placeholder(name.split()[0], size=(500, 500), color_index=i + 3),
                )

    def _seed_news(self):
        entries = [
            (
                "We're opening a second studio in Alexandria",
                "A new space for larger productions, opening Q3.",
            ),
            (
                "Featured in Campaign Middle East",
                "Our latest work for Nova Foods was featured in this month's issue.",
            ),
            (
                "Hiring: Senior Producer",
                "We're looking for a senior producer with 5+ years of commercial experience.",
            ),
        ]
        for i, (name, desc) in enumerate(entries):
            news, created = News.objects.get_or_create(
                name=name, defaults={"description": desc, "is_published": True}
            )
            if created:
                for j in range(2):
                    img = NewsImage(news=news, caption=f"Image {j + 1}", order=j)
                    img.image.save(
                        f"news_{i}_{j}.png",
                        placeholder(
                            f"News {i + 1}.{j + 1}", size=(900, 550), color_index=i + j + 4
                        ),
                    )
                    img.save()

    def _seed_projects(self):
        entries = [
            (
                "Nova Foods — Summer Campaign",
                "A three-week shoot across Cairo and Alexandria for Nova Foods' summer launch. "
                "Directed, produced, and edited in-house.",
            ),
            (
                "Cairo Motors — Launch Film",
                "Hero launch film for the Cairo Motors EV lineup. Shot on location in the Western Desert.",
            ),
            (
                "Lumen Apparel — Lookbook",
                "Seasonal lookbook and 30-second spot for Lumen's fall collection.",
            ),
            (
                "Orbit Telecom — Brand Refresh",
                "Full brand refresh including new visual identity, launch film, and social-first cutdowns.",
            ),
        ]
        for i, (name, bio) in enumerate(entries):
            project, created = Project.objects.get_or_create(
                name=name, defaults={"bio": bio, "order": i}
            )
            if created:
                for j in range(3):
                    pi = ProjectImage(project=project, caption=f"Still {j + 1}", order=j)
                    pi.image.save(
                        f"project_{i}_{j}.png",
                        placeholder(
                            f"{name.split()[0]} {j + 1}", size=(1200, 700), color_index=i + j
                        ),
                    )
                    pi.save()

    def _seed_contact_messages(self):
        if ContactMessage.objects.exists():
            return
        ContactMessage.objects.create(
            name="Sara Elhadidy",
            email="sara@example.com",
            subject="Partnership inquiry",
            message="Hi — we'd love to chat about a campaign for Q4. Can we schedule a call?",
        )
        ContactMessage.objects.create(
            name="Mark Johnson",
            email="mark@example.com",
            subject="Production quote",
            message="Looking for a quote on a 60-second commercial shoot. Timeline is flexible.",
        )
