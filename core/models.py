from django.db import models


DEFAULT_HERO_DESCRIPTION = (
    "A production company based in Iraq, Baghdad, specialized in producing "
    "documentary works. We are dedicated to capturing real-life stories and "
    "presenting them in a compelling and thought-provoking manner. Our mission "
    "is to shed light on important issues and bring untold narratives to the "
    "forefront of the global audience"
)


class HeroDescription(models.Model):
    text = models.TextField(default=DEFAULT_HERO_DESCRIPTION)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Description"
        verbose_name_plural = "Hero Description"

    def __str__(self):
        return "Hero description"


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    body_text = models.TextField(blank=True, help_text="Text shown under the hero.")
    background_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    background_video = models.FileField(upload_to="hero/", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return self.title


class Client(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to="clients/", blank=True, null=True)
    website = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class BehindTheScenesImage(models.Model):
    image = models.ImageField(upload_to="bts/")
    caption = models.CharField(max_length=200, blank=True)
    animation = models.CharField(
        max_length=40,
        default="fade-in",
        help_text="Animation class name used in the template (e.g. fade-in, slide-up).",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Behind The Scenes Image"

    def __str__(self):
        return self.caption or f"BTS #{self.pk}"


class FooterInfo(models.Model):
    company_name = models.CharField(max_length=150, blank=True)
    logo = models.ImageField(upload_to="site/", blank=True, null=True)
    favicon = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text="Browser tab icon. Should be a small square image with transparent background.",
    )
    tagline = models.CharField(max_length=250, blank=True)
    address = models.CharField(max_length=250, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    copyright_text = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = "Footer"
        verbose_name_plural = "Footer"

    def __str__(self):
        return self.company_name


class AboutInfo(models.Model):
    who_we_are_title = models.CharField(max_length=200, default="Who We Are")
    who_we_are_body = models.TextField(blank=True)
    what_we_do_title = models.CharField(max_length=200, default="What We Do")
    what_we_do_body = models.TextField(blank=True)
    background_image = models.ImageField(
        upload_to="about/",
        blank=True,
        null=True,
        help_text="Background image behind the Who We Are / What We Do section.",
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "About Info"
        verbose_name_plural = "About Info"

    def __str__(self):
        return "About content"


class Post(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    video = models.FileField(upload_to="posts/", blank=True, null=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class BTSGalleryImage(models.Model):
    """Independent gallery for the dedicated /behind-the-scenes/ page.
    Not connected to BehindTheScenesImage (which feeds the home slider)."""

    image = models.ImageField(upload_to="bts-gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "BTS Gallery Image"
        verbose_name_plural = "BTS Gallery Images"

    def __str__(self):
        return self.caption or f"BTS Gallery #{self.pk}"


class CastingPage(models.Model):
    """Singleton-style content for the /casting/ page."""

    background_image = models.ImageField(
        upload_to="casting/",
        blank=True,
        null=True,
    )
    description = models.TextField(
        blank=True,
        help_text="Text shown over the background image (bottom-left).",
    )
    button_label = models.CharField(max_length=100, default="View on Instagram")
    button_url = models.URLField(default="https://www.instagram.com/bsrcast/")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Casting Page"
        verbose_name_plural = "Casting Page"

    def __str__(self):
        return "Casting page"
