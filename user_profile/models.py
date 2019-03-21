from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return str(self.__dict__)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', default='uploads/no-img.png')
    sex = models.CharField(max_length=10, choices=sex_choices)
    contact_no = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.user)


class Doctor(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    speciality = models.TextField(blank=True, null=True)
    qualification = models.TextField(blank=True, null=True)
    fees = models.IntegerField(blank=True, null=True)
    bmdc = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.profile)


class Disease(models.Model):
    name = models.CharField(max_length=100)
    lab_report = models.FileField(upload_to='uploads/', default='uploads/default_pic.png')
    prescription = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Patient(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    diseases = models.ManyToManyField(Disease,blank=True)
    blood_group = models.CharField(max_length=10, null=True, blank=True)
    blood_pressure = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return str(self.profile)


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    address = models.TextField(null=True,blank=True)
    location = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    patient_amount = models.IntegerField()
    patients = models.ManyToManyField(Patient,blank=True)

    def __str__(self):
        return str(self.doctor)
