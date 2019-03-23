from django.db import models


class DiseaseManager(models.Manager):
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
