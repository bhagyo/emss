from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, ListSerializer
from rest_framework.fields import BooleanField, CharField, DateField, EmailField, ImageField
from rest_framework.exceptions import NotFound, ValidationError

from .models import Address, Appointment, Disease, Doctor, Patient, Profile


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        exclude = ['id']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        read_only_fields = ['username']


class RegisterSerializer(Serializer):
    first_name = CharField(label='First Name', max_length=30, required=False, allow_null=True, allow_blank=True,
                           trim_whitespace=True)
    last_name = CharField(label='Last Name', max_length=150, required=False, allow_null=True, allow_blank=True,
                          trim_whitespace=True)
    username = CharField(label='Username', max_length=150, required=True, allow_null=False, allow_blank=False,
                         trim_whitespace=True)
    email = EmailField(label='Email', required=True, allow_null=False, allow_blank=False, trim_whitespace=True)
    password = CharField(label='Password', max_length=150, required=True, allow_null=False, allow_blank=False)
    password_confirmation = CharField(label='Confirm Password', max_length=150, required=True, allow_null=False,
                                      allow_blank=False)
    address = AddressSerializer()
    date_of_birth = DateField(label='Date Of Birth', required=True, allow_null=False)
    is_doctor = BooleanField(label='Is Doctor', default=False)

    def validate_username(self, username):
        user_qs = User.objects.filter(username=username)
        if user_qs:
            raise ValidationError('Username already exists')
        return username

    def validate_email(self, email):
        user_qs = User.objects.filter(email=email)
        if user_qs:
            raise ValidationError('Email already exists')
        return email

    def validate_password_confirmation(self, password_confirmation):
        data = self.get_initial()
        password = data.get('password')

        if password != password_confirmation:
            raise ValidationError('Passwords did not match')
        return password_confirmation

    def create(self, validated_data):

        user_data = dict()
        user_data['username'] = validated_data['username']
        user_data['email'] = validated_data['email']
        user_data['password'] = validated_data['password']
        user_data['first_name'] = validated_data['first_name']
        user_data['last_name'] = validated_data['last_name']

        user = User.objects.create_user(**user_data)

        user_address_data = validated_data['address']
        address = Address.objects.create(**user_address_data)

        user_profile_data = dict()
        user_profile_data['date_of_birth'] = validated_data.get('date_of_birth')
        user_profile_data['user'] = user
        user_profile_data['address'] = address

        profile = Profile.objects.create(**user_profile_data)

        if validated_data['is_doctor']:
            Doctor.objects.create(profile=profile)
        else:
            Patient.objects.create(profile=profile)

        return validated_data

    def update(self, instance, validated_data):
        return instance


class LoginSerializer(Serializer):
    # token = CharField(allow_blank=True, read_only=True)
    username = CharField(label='Username', max_length=150, required=True, allow_null=False, allow_blank=False,
                         trim_whitespace=True)
    password = CharField(label='Password', max_length=150, required=True, allow_null=False, allow_blank=False)

    def validate(self, data):
        username = data.get('username', '')
        password = data.get('password', '')

        if not username:
            raise ValidationError('Username is required')
        if not password:
            raise ValidationError('Password is required')

        user = User.objects.filter(username=username).first()

        if user is None:
            raise NotFound('User not found')

        return data

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        return instance


class ProfileSerializer(ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()

    class Meta:
        model = Profile
        exclude = ['id']


class DoctorSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Doctor
        exclude = ['id']

    def update(self, instance, validated_data):
        profile_data = validated_data['profile']
        user_data = profile_data['user']
        user_address = profile_data['address']

        instance.profile.user.first_name = user_data.get('first_name', instance.profile.user.first_name)
        instance.profile.user.last_name = user_data.get('last_name', instance.profile.user.last_name)
        instance.profile.user.email = user_data.get('email', instance.profile.user.email)
        instance.profile.user.save()

        instance.profile.address.division = user_address.get('division', instance.profile.address.division).lower()
        instance.profile.address.district = user_address.get('district', instance.profile.address.district).lower()
        instance.profile.address.upozilla = user_address.get('upozilla', instance.profile.address.upozilla).lower()
        instance.profile.address.address = user_address.get('address', instance.profile.address.address).lower()
        instance.profile.address.save()

        instance.profile.image = profile_data.get('image', instance.profile.image)
        instance.profile.sex = profile_data.get('sex', instance.profile.sex)
        instance.profile.contact_no = profile_data.get('contact_no', instance.profile.contact_no)
        instance.profile.date_of_birth = profile_data.get('date_of_birth', instance.profile.date_of_birth)
        instance.profile.save()

        instance.speciality = validated_data.get('speciality', instance.speciality).lower()
        instance.qualification = validated_data.get('qualification', instance.qualification).lower()
        instance.fees = validated_data.get('fees', instance.fees)
        instance.bmdc = validated_data.get('bmdc', instance.bmdc)
        instance.save()

        return instance

    def create(self, validated_data):
        return validated_data


class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        fields = '__all__'
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.lab_report = validated_data.get('lab_report',instance.lab_report)
        instance.prescription = validated_data.get('prescription',instance.prescription)
        instance.start_time = validated_data.get('start_time',instance.start_time)
        instance.end_time = validated_data.get('end_time',instance.end_time)
        instance.symptoms = validated_data.get('name',instance.symptoms)
        instance.save()
        return instance
    def create(self, validated_data):
        return validated_data

'''
class PatientSerializer(ListSerializer):
    class Meta:
        model = Patient
        field = ['diseases']
    def update(self, instance, validated_data):
        disease_mapping = {disease.id: disease for disease in instance}
        data_mapping = {item['id']: item for item in validated_data}
        keep_disease = []
        for disease_id,data in data_mapping.items():
            disease = disease_mapping.get(disease_id,None)
            if disease is None:
                keep_disease(self.child.create(data))
            else:
                keep_disease.append(self.child.update(disease,data))
        for disease_id, disease in disease_mapping.items():
            if disease_id not in data_mapping:
                disease.delete()
        return keep_disease

'''


class PatientSerializer(ModelSerializer):
    profile = ProfileSerializer()
    diseases = DiseaseSerializer(many=True)

    class Meta:
        model = Patient
        fields = '__all__'

    def update(self, instance, validated_data):
        profile_data = validated_data['profile']
        user_data = profile_data['user']
        user_address = profile_data['address']

        instance.profile.user.first_name = user_data.get('first_name', instance.profile.user.first_name)
        instance.profile.user.last_name = user_data.get('last_name', instance.profile.user.last_name)
        instance.profile.user.email = user_data.get('email', instance.profile.user.email)
        instance.profile.user.save()

        instance.profile.address.division = user_address.get('division', instance.profile.address.division).lower()
        instance.profile.address.district = user_address.get('district', instance.profile.address.district).lower()
        instance.profile.address.upozilla = user_address.get('upozilla', instance.profile.address.upozilla).lower()
        instance.profile.address.address = user_address.get('address', instance.profile.address.address).lower()
        instance.profile.address.save()

        instance.profile.sex = profile_data.get('sex', instance.profile.sex)
        instance.profile.contact_no = profile_data.get('contact_no', instance.profile.contact_no)
        instance.profile.date_of_birth = profile_data.get('date_of_birth', instance.profile.date_of_birth)
        instance.profile.save()

        '''
        user_disease = validated_data.pop('diseases')
        keep_disease = []
        for disease in user_disease:
            if "id" in disease.keys():
                if Disease.objects.filter(id=disease["id"]).exist():
                    c = Disease.objects.get(id = disease["id"])
                    c.name = Disease.get('name',c.name)
                    c.lab_report = Disease.get('lab_report',c.lab_report)
                    c.prescription = Disease.get('prescription',c.prescription)
                    c.start_time = Disease.get('start_time',c.start_time)
                    c.end_time = Disease.get('end_time',c.end_time)
                    c.symptoms = Disease.get('symptoms',c.symptoms)
                    c.save()
                    keep_disease.append(c)
                else:
                    continue
            else:
                c = Disease.objects.create(**disease, patient=instance)
                keep_disease.append(c.id)
        for disease in instance.diseases:
            if disease.id not in keep_disease:
                disease.delete()
        instance.diseases=keep_disease
        '''

        disease_mapping = {disease.id: disease for disease in instance}
        data_mapping = {item['id']: item for item in validated_data}
        keep_disease = []
        for disease_id, data in data_mapping.items():
            disease = disease_mapping.get(disease_id, None)
            if disease is None:
                keep_disease(self.child.create(data))
            else:
                keep_disease.append(self.child.update(disease, data))
        for disease_id, disease in disease_mapping.items():
            if disease_id not in data_mapping:
                disease.delete()

        instance.blood_group = validated_data.get('blood_group', instance.blood_group.lower()).lower()
        instance.blood_pressure = validated_data.get('blood_pressure', instance.blood_pressure)
        instance.save()

        return instance

    def create(self, validated_data):
        diseases = [Disease(**item) for item in validated_data]
        return Disease.objects.bulk_create(diseases)


class AppointmentSerializer(ModelSerializer):
    patients = PatientSerializer(many=True,allow_null=True)
    class Meta:
        model = Appointment
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address).lower()
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.patients = validated_data.get('patients',instance.patients)
        instance.patient_amount = validated_data.get('patient_amount', instance.patient_amount)
        instance.save()
        return instance

    def create(self, validated_data):
        return validated_data
