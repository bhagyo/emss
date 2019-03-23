from django.db import models


class AddressManager(models.Manager):
    def create_obj(self, data):
        obj_data = dict()
        obj_data['division'] = data.get('division')
        obj_data['district'] = data.get('district')
        obj_data['upozilla'] = data.get('upozilla')
        obj_data['address'] = data.get('address')
        obj = self.create(**obj_data)
        return obj


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
