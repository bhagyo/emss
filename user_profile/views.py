from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import (HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView

from .models import Doctor, Patient, Address, Appointment, Disease
from .serializers import (RegisterSerializer, LoginSerializer, DoctorSerializer, PatientSerializer, AddressSerializer,
                          DiseaseSerializer, AppointmentSerializer)


class DoctorListAPIView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientListAPIView(ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny, ]


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
            else:
                raise AuthenticationFailed(detail='Password did not match', code=HTTP_401_UNAUTHORIZED)
            return Response({'message': 'User logged in'}, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class AddressListAPIView(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class DiseaseListAPIView(ListAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer


class DiseaseRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer


class DiseaseCreateAPIView(CreateAPIView):
    queryset = Disease.objects.all()
    serializer_class = DiseaseSerializer


class DoctorSearchAPIView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('speciality', 'profile__address__district',)


class AppointmentListAPIView(ListAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmentCreateAPIView(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
