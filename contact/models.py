from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-sent_at"]
# this is the string representation of the model, it will be used in the admin interface and when printing the object
    def __str__(self):
        return f"{self.name} — {self.subject or '(no subject)'}"
    
