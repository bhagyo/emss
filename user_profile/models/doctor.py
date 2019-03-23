from django.db import models
from .profile import Profile


class DoctorManager(models.Manager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['profile'] = Profile.objects.create_obj(data.get('profile', dict()))
        obj_data['speciality'] = data.get('speciality')
        obj_data['qualification'] = data.get('qualification')
        obj_data['fees'] = data.get('fees')
        obj_data['bmdc'] = data.get('bmdc')
        obj = self.create(**obj_data)
        return obj


class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    speciality = models.TextField(blank=True, null=True)
    qualification = models.TextField(blank=True, null=True)
    fees = models.IntegerField(blank=True, null=True)
    bmdc = models.IntegerField(blank=True, null=True)

    objects = DoctorManager()

    def __str__(self):
        return str(self.profile)

    def update(self, data):
        self.profile = self.profile.update(data.get('profile', dict()))

        self.speciality = data.get('speciality', self.speciality)
        self.qualification = data.get('qualification', self.qualification)
        self.fees = data.get('fees', self.fees)
        self.bmdc = data.get('bmdc', self.bmdc)
        self.save()
        return self
