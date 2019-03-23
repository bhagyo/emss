from django.db import models

from .address import Address
from .doctor import Doctor
from .patient import Patient


class AppointmentManager(models.Manager):
    def create_obj(self, data,doctors_id3):
        obj_data = dict()
        obj_data['doctor'] = Doctor.objects.get(id=doctors_id3)
        #obj_data['doctor'] = Doctor.objects.create_obj(data.get('doctor', dict()))
        #obj_data['address'] = Address.objects.create_obj(data.get('address', dict()))
        obj_data['location'] = data.get('location')
        obj_data['start_time'] = data.get('start_time')
        obj_data['end_time'] = data.get('end_time')
        obj_data['patient_amount'] = data.get('patient_amount')
        obj = self.create(**obj_data)

        patients = data.get('patients', list())
        for _patient in patients:
            patient = Patient.objects.get(id=_patient)
            obj.patients.add(patient)
            obj.save()
        return obj


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    #address = models.ForeignKey(Address, on_delete=models.CASCADE)
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

        #self.address = data.get('address', self.address)
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
