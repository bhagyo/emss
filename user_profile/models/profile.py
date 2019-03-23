from django.db import models
from django.contrib.auth.models import User

from .address import Address

MALE = 'Male'
FEMALE = 'Female'
sex_choices = (
    (MALE, MALE),
    (FEMALE, FEMALE)
)


class ProfileManager(models.Manager):
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


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/', default='uploads/no-img.jpg')
    sex = models.CharField(max_length=10, choices=sex_choices,null=True,blank=True)
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
