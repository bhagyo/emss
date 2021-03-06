from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from datetime import datetime
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED)

from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView

from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .models import Doctor, Patient, Address, Appointment, Disease
from .serializers import (RegisterSerializer, LoginSerializer, DoctorSerializer, PatientSerializer, AddressSerializer,
                          DiseaseSerializer, AppointmentSerializer, AppointmentCreateSerializer,
                          AppointmentSurveySerializer)


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


class DoctorLoginAPIView(APIView):
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
            return Response({'message': 'User logged in', 'user_id': user.profile.doctor.id}, status=HTTP_200_OK)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PatientLoginAPIView(APIView):
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
            return Response({'message': 'User logged in', 'user_id': user.profile.patient.id}, status=HTTP_200_OK)

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
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('doctor__id',)


class AppointmentCreateAPIView(CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentCreateSerializer


class AppointmentGetAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer


class AppointmenSurveytAPIView(APIView):

    def get(self, request, format=None):
        speciality = request.query_params['speciality']
        duration = request.query_params['duration']
        timestamp = datetime.now().timestamp()
        duration = int(duration) * 24 * 60 * 60
        current_time = datetime.fromtimestamp(timestamp - duration)
        appointments = Appointment.objects.filter(start_time__gte=current_time,
                                                  doctor__speciality__icontains=speciality)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
