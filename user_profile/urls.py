from django.urls import path, include
from django.conf.urls import include
from .views import (UserCreateAPIView, LoginAPIView, DoctorListAPIView, AddressListAPIView,
                    AddressRetrieveAPIView, DoctorRetrieveAPIView, PatientListAPIView, PatientRetrieveAPIView,
                    DiseaseListAPIView, DiseaseRetrieveAPIView, DiseaseCreateAPIView, DoctorSearchAPIView,
                    AppointmentListAPIView, AppointmentCreateAPIView, AppointmentGetAPIView, AppointmenSurveytAPIView
                    )

''''
from rest_framework import routers
router.register('v1/doctorextra/', DoctorSearchAPIView.as_view(),name='doctorextra')
jodi uporer ta likhi tobe urlpatterns er vitore likhte hobe
path('',include(router.urls))
'''

urlpatterns = [

    path('doctors/<int:pk>/', DoctorRetrieveAPIView.as_view(), name='doctors_retrieve'),
    path('doctors/', DoctorListAPIView.as_view(), name='doctors_list'),

    path('patients/<int:pk>/', PatientRetrieveAPIView.as_view(), name='patients_retrieve'),
    path('patients/', PatientListAPIView.as_view(), name='patients_list'),

    path('register/', UserCreateAPIView.as_view(), name='user_register'),

    path('login/', LoginAPIView.as_view(), name='user_login'),

    path('address/', AddressListAPIView.as_view(), name='address'),
    path('address/<int:pk>', AddressRetrieveAPIView.as_view(), name='address_retrive'),

    path('disease/', DiseaseListAPIView.as_view(), name='disease'),
    path('disease/<int:pk>', DiseaseRetrieveAPIView.as_view(), name='disease_retrive'),
    path('disease/create/', DiseaseCreateAPIView.as_view(), name='disease_create'),

    path('doctorsearch/', DoctorSearchAPIView.as_view(), name='doctorsearch'),

    path('appointmentlist/', AppointmentListAPIView.as_view(), name='AppointmentListAPIView'),
    path('appointmentcreate/', AppointmentCreateAPIView.as_view(), name='appointmentcreate'),
    path('appointmentget/<int:pk>', AppointmentGetAPIView.as_view(), name='appointmentget'),

    path('surveylist/', AppointmenSurveytAPIView.as_view(), name='surveylist'),
]
