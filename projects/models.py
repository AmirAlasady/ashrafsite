from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True, help_text="Project description shown above the video.")
    video = models.FileField(
        upload_to="projects/videos/",
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

    def __str__(self):
        return self.name


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="projects/images/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.project.name} image #{self.pk}"
