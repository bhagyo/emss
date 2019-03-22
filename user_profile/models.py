from django.db import models
from django.contrib.auth.models import User

from .managers import AddressManager, ProfileManager, DoctorManager, DiseaseManager, PatientManager, AppointmentManager

# Create your models here.

MALE = 'Male'
FEMALE = 'Female'
sex_choices = (
    (MALE, MALE),
    (FEMALE, FEMALE)
)


class Address(models.Model):
    division = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    upozilla = models.CharField(max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    objects = AddressManager()

    def __str__(self):
        return str(self.__dict__)

    def update(self, data):
        self.division = data.get('division', self.division)
        self.district = data.get('district', self.district)
        self.upozilla = data.get('upozilla', self.upozilla)
        self.address = data.get('address', self.address)
        self.save()
        return self


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', default='uploads/no-img.jpg')
    sex = models.CharField(max_length=10, choices=sex_choices)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        return str(self.user)

    def update(self, data):
        self.user = self.update_user(data.get('user', dict()))
        self.address = self.address.update(data.get('address', dict()))

        self.image = data.get('image', self.image)
        self.sex = data.get('sex', self.sex)
        self.contact_no = data.get('contact_no', self.contact_no)
        self.date_of_birth = data.get('date_of_birth', self.date_of_birth)
        self.save()
        return self

    def update_user(self, data):
        self.user.first_name = data.get('first_name', self.user.first_name)
        self.user.last_name = data.get('last_name', self.user.last_name)
        self.user.save()
        return self.user


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


class Disease(models.Model):
    name = models.CharField(max_length=100)
    lab_report = models.FileField(upload_to='uploads/', default='uploads/no-img.jpg')
    prescription = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)

    objects = DiseaseManager()

    def __str__(self):
        return str(self.name)

    def update(self, data):
        self.name = data.get('name', self.name)
        self.lab_report = data.get('lab_report', self.lab_report)
        self.prescription = data.get('prescription', self.prescription)
        self.start_time = data.get('start_time', self.start_time)
        self.end_time = data.get('end_time', self.end_time)
        self.symptoms = data.get('symptoms', self.symptoms)
        self.save()
        return self


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


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    patient_amount = models.IntegerField()
    patients = models.ManyToManyField(Patient)

    objects = AppointmentManager()

    def __str__(self):
        return str(self.doctor)

    def update(self, data):
        self.doctor = self.doctor.update(data.get('doctor', dict()))

        self.address = data.get('address', self.address)
        self.location = data.get('location', self.location)
        self.start_time = data.get('start_time', self.start_time)
        self.end_time = data.get('end_time', self.end_time)
        self.patient_amount = data.get('patient_amount', self.patient_amount)

        self.update_patients(data.get('patients', list()))
        self.save()
        return self

    def update_patients(self, data):
        for _patient in data:
            try:
                patient = Patient.objects.get(id=_patient['id'])
                self.patients.add(patient)
            except:
                pass

        return self
