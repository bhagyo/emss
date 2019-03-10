from django.urls import path

from .views import (UserCreateAPIView, LoginAPIView, DoctorListAPIView,
                    DoctorRetrieveAPIView, PatientListAPIView, PatientRetrieveAPIView)

urlpatterns = [
    # path('users/<int:pk>/', UserListSingleAPIView.as_view(), name='user_single'),
    # path('users/', UserListAPIView.as_view(), name='user'),
    path('doctors/<int:pk>/', DoctorRetrieveAPIView.as_view(), name='doctors_retrieve'),
    path('doctors/', DoctorListAPIView.as_view(), name='doctors_list'),
    path('patients/<int:pk>/', PatientRetrieveAPIView.as_view(), name='patients_retrieve'),
    path('patients/', PatientListAPIView.as_view(), name='patients_list'),
    path('register/', UserCreateAPIView.as_view(), name='user_register'),
    path('login/', LoginAPIView.as_view(), name='user_login'),

]
