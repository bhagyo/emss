from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', default='uploads/no-img.png')
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    bmdc = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.profile)


class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    disease = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.profile)
