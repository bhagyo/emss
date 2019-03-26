from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.fields import BooleanField, CharField, DateField, EmailField, IntegerField, ListField
from rest_framework.exceptions import NotFound, ValidationError

from .models import Address, Appointment, Disease, Doctor, Patient, Profile


class AddressSerializer(ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

    def create(self, validated_data):
        Address.objects.create_obj(validated_data)
        return validated_data


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email']
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
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

    def create(self, validated_data):
        Profile.objects.create_obj(validated_data)
        return validated_data


class DoctorSerializer(ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Doctor
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

    def create(self, validated_data):
        Doctor.objects.create_obj(validated_data)
        return validated_data


class DiseaseSerializer(ModelSerializer):
    class Meta:
        model = Disease
        # fields = ['__all__']
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

    def create(self, validated_data):
        Disease.objects.create_obj(validated_data)
        return validated_data


class PatientSerializer(ModelSerializer):
    profile = ProfileSerializer()
    diseases = DiseaseSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        # fields = '__all__'
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance

    def create(self, validated_data):
        Patient.objects.create_obj(validated_data)
        return validated_data


class AppointmentSerializer(ModelSerializer):
    # doctor = DoctorSerializer()
    # address = AddressSerializer()
    patients = PatientSerializer(many=True, read_only=True)
    patients_id = ListField(child=IntegerField(), default=list, write_only=True)

    # TODO: add write-only field

    class Meta:
        model = Appointment
        fields = ['doctor', 'patients', 'patients_id', 'location', 'id', 'start_time', 'end_time', 'patient_amount']
        # depth=3

    def update(self, instance, validated_data):
        # validated_data['patient'] = Patient.objects.get(id=patient_id)
        print(validated_data)
        instance.update(validated_data)
        return instance

    def create(self, validated_data):
        # validated_data['doctor'] = Doctor.objects.get(id=doctor_id2)
        Appointment.objects.create_obj(validated_data)
        return validated_data


class AppointmentCreateSerializer(ModelSerializer):
    # doctor = DoctorSerializer()
    # address = AddressSerializer()
    patients = PatientSerializer(many=True, read_only=True)

    class Meta:
        model = Appointment
        # fields = ['__all__']
        fields = '__all__'

    def update(self, instance, validated_data):
        validated_data['patient'] = Doctor.objects.get(id=patient_id)
        instance.update(validated_data)
        return instance

    def get(self, validated_data):
        validated_data['doctor'] = Doctor.objects.get(id=doctor_id2)
        Appointment.objects.create_obj(validated_data)
        return validated_data


class AppointmentSurveySerializer(ModelSerializer):
    doctor = DoctorSerializer()

    class Meta:
        model = Appointment
        fields = '__all__'
        depth = 2
