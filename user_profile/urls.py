from django.urls import path

from .views import (UserCreateAPIView, LoginAPIView, DoctorListAPIView, AddressListAPIView,
                    AddressRetrieveAPIView, DoctorRetrieveAPIView, PatientListAPIView, PatientRetrieveAPIView,
                    DiseaseListAPIView, DiseaseRetrieveAPIView
                    )

urlpatterns = [
    # path('users/<int:pk>/', UserListSingleAPIView.as_view(), name='user_single'),
    # path('users/', UserListAPIView.as_view(), name='user'),
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

]
