from django.db import models


class AcademyItem(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, help_text="Description shown above the video.")
    video = models.FileField(
        upload_to="academy/videos/",
        blank=True,
        null=True,
        help_text="Shown directly under the description.",
    )
    video_url = models.URLField(
        blank=True,
        help_text="Optional external video URL (YouTube, Vimeo). Used if no uploaded video.",
    )
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "Academy Item"
        verbose_name_plural = "Academy Items"

    def __str__(self):
        return self.name


class AcademyItemImage(models.Model):
    item = models.ForeignKey(AcademyItem, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="academy/images/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.item.name} image #{self.pk}"
