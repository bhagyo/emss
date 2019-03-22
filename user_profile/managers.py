from django.db import models
from django.contrib.auth.models import User

from .models import Address, Appointment, Disease, Doctor, Patient, Profile


class BaseManager(models.Manager):
    pass


class AddressManager(BaseManager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['division'] = data.get('division')
        obj_data['district'] = data.get('district')
        obj_data['upozilla'] = data.get('upozilla')
        obj_data['address'] = data.get('address')
        obj = self.create(**obj_data)
        return obj


class ProfileManager(BaseManager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['user'] = self.create_user_obj(data.get('user', dict()))
        obj_data['address'] = Address.objects.create_obj(data.get('address', dict()))
        obj_data['image'] = data.get('image')
        obj_data['sex'] = data.get('sex')
        obj_data['contact_no'] = data.get('contact_no')
        obj_data['date_of_birth'] = data.get('date_of_birth')
        obj = self.create(**obj_data)
        return obj

    def create_user_obj(self, data):
        obj_data = dict()
        obj_data['first_name'] = data.get('first_name')
        obj_data['last_name'] = data.get('last_name')
        obj_data['username'] = data.get('username')
        obj_data['email'] = data.get('email')
        obj_data['password'] = data.get('password')
        obj = User.objects.create_user(**obj_data)
        return obj


class DoctorManager(BaseManager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['profile'] = Profile.objects.create_obj(data.get('profile', dict()))
        obj_data['speciality'] = data.get('speciality')
        obj_data['qualification'] = data.get('qualification')
        obj_data['fees'] = data.get('fees')
        obj_data['bmdc'] = data.get('bmdc')
        obj = self.create(**obj_data)
        return obj


class DiseaseManager(BaseManager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['name'] = data.get('name', dict())
        obj_data['lab_report'] = data.get('lab_report')
        obj_data['prescription'] = data.get('prescription')
        obj_data['start_time'] = data.get('start_time')
        obj_data['end_time'] = data.get('end_time')
        obj_data['symptoms'] = data.get('symptoms')
        obj = self.create(**obj_data)
        return obj


class PatientManager(BaseManager):
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


class AppointmentManager(BaseManager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['doctor'] = Doctor.objects.create_obj(data.get('doctor', dict()))
        obj_data['address'] = Address.objects.create_obj(data.get('address', dict()))
        obj_data['location'] = data.get('location')
        obj_data['start_time'] = data.get('start_time')
        obj_data['end_time'] = data.get('end_time')
        obj_data['patient_amount'] = data.get('patient_amount')
        obj = self.create(**obj_data)

        patients = data.get('patients', list())
        for _patient in patients:
            patient = Patient.objects.create_obj(_patient)
            obj.patients.add(patient)
            obj.save()
        return obj
