import django
from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS, BasePermission
from .models import *
from .serializers import *
from .email import sendOTP
from functools import partial
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken

import json
import threading

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)
class EmailThread(threading.Thread):
    def __init__(self, sendOTP):
        self.sendOTP = sendOTP
        threading.Thread.__init__(self)

    def run(self):
        self.sendOTP()

       
class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class MyPermission(permissions.BasePermission):
    def __init__(self, allowed_methods):
        super().__init__()
        self.allowed_methods = allowed_methods

    def has_permission(self, request, view):
        return request.method in self.allowed_methods

class UserRegister(APIView):
    # permission_classes = [ReadOnly]
    def post(self, request):
        try:
            data = request.data
            serializer = RegitserSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                sendOTP(data['email'])
                return Response({
                    'status': 200,
                    'message': 'Verification code sent on the mail address. Please check',
                })
            return Response({
                'status': 400,
                'message': 'Something went wrong',
                'data': serializer.errors
            })

        except Exception as e:
            print(e)

class LoginUser(APIView):
    # permission_classes = (partial(MyPermission, ['GET', 'POST', 'HEAD']),)
    def post(self, request):
        # try:
            data = request.data
            serializer = LoginSerializer(data=request.data)
            print(data['email'],"--------------")
            # verify_user = RegisterUser.objects.filter(email = data['email'])
            # if not verify_user:
            #     user = RegisterUser(email = data['email'])
            #     user.save()
            # else:
            #     user = verify_user[0]
            user, created = get_user_model().objects.get_or_create(email=data['email'])
            sendOTP(user)
            return Response({
            'status': 200,
            'message': 'Verification code sent on the mail address. Please check',
            # 'data': serializer.data,
            })
        # except: 
        #     return Response({
        #     'status': 400,
        #     'message': 'Something went wrong',
        #     })


