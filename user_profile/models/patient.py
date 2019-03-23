from django.db import models

from .profile import Profile
from .disease import Disease


class PatientManager(models.Manager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['profile'] = Profile.objects.create_obj(data.get('profile', dict()))
        obj_data['blood_group'] = data.get('blood_group')
        obj_data['blood_pressure'] = data.get('blood_pressure')
        obj = self.create(**obj_data)

        diseases = data.get('diseases', list())
        for _disease in diseases:
            disease = Disease.objects.create_obj(_disease)
            obj.diseases.add(disease)
            obj.save()
        return obj


class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    diseases = models.ManyToManyField(Disease, blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    blood_pressure = models.CharField(max_length=10, blank=True, null=True)

    objects = PatientManager()

    def __str__(self):
        return str(self.profile)

    def update(self, data):
        self.profile = self.profile.update(data.get('profile', dict()))
        self.update_diseases(data.get('diseases', list()))

        self.blood_group = data.get('blood_group', self.blood_group)
        self.blood_pressure = data.get('blood_pressure', self.blood_pressure)
        self.save()
        return self

    def update_diseases(self, data):
        for _disease in data:
            try:
                disease = Disease.objects.get(id=_disease['id'])
                disease.update(_disease)
            except:
                pass

        return self
