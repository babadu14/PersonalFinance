from django.shortcuts import render
from rest_framework import mixins, viewsets
from users.serializers import (RegisterSerielizer, UserSerializer, 
                               PasswordResetConfirmSerializer, ProfileSerializer,
                               EmailCodeResendSerializer, )

# Create your views here.
