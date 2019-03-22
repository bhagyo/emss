from django.db import models


class BaseManager(models.Manager):
    pass


class AddressManager(BaseManager):
    pass


class ProfileManager(BaseManager):
    pass


class DoctorManager(BaseManager):
    pass


class DiseaseManager(BaseManager):
    pass


class PatientManager(BaseManager):
    pass


class AppointmentManager(BaseManager):
    pass
