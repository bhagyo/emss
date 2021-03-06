from django.db import models

from .address import Address
from .doctor import Doctor
from .patient import Patient


class AppointmentManager(models.Manager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['doctor'] = Doctor.objects.get(id=data.id)
        # obj_data['doctor'] = Doctor.objects.create_obj(data.get('doctor', dict()))
        # obj_data['address'] = Address.objects.create_obj(data.get('address', dict()))
        obj_data['location'] = data.get('location')
        obj_data['start_time'] = data.get('start_time')
        obj_data['end_time'] = data.get('end_time')
        obj_data['patient_amount'] = data.get('patient_amount')
        obj = self.create(**obj_data)
        return obj


'''
    def update(self, validated_data):
        validated_data['patient'] = Patient.objects.get(id=doctor_id2)
        patients = data.get('patients', list())
        for _patient in patients:
            patient = Patient.objects.get(id=p)
            obj.patients.add(patient)
            obj.save()
            break
        return obj
'''


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    # address = models.ForeignKey(Address, on_delete=models.CASCADE)
    location = models.CharField(max_length=50, null=True, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    patient_amount = models.IntegerField()
    patients = models.ManyToManyField(Patient)

    objects = AppointmentManager()

    def __str__(self):
        return str(self.doctor)

    def update(self, data):
        # self.doctor = self.doctor.update(data.get('doctor', dict()))
        self.doctor = Doctor.objects.get(id=data['doctor'].id)
        print(data)

        # self.address = data.get('address', self.address)
        self.location = data.get('location', self.location)
        self.start_time = data.get('start_time', self.start_time)
        self.end_time = data.get('end_time', self.end_time)
        self.patient_amount = data.get('patient_amount', self.patient_amount)

        self.update_patients(data.get('patients_id', list()))
        self.save()
        return self

    def update_patients(self, data):
        for _patient_id in data:
            try:
                patient = Patient.objects.get(id=_patient_id)
                self.patients.add(patient)
            except:
                pass

        return self
