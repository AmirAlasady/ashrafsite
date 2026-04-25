from django.db import models


class Member(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    bio = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.name} — {self.role}"
