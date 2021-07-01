from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()
    profile_image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.name

