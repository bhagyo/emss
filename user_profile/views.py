from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView

from .models import Doctor, Patient, Profile
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer, DoctorSerializer, PatientSerializer


"""class UserListSingleAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer"""


class DoctorListAPIView(ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class DoctorRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientListAPIView(ListAPIView):
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
