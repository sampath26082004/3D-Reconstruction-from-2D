from django.db import models
from django.contrib.auth.models import User

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='uploads/')
    # Add any other fields you need


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

