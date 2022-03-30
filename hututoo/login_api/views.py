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
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken




class LoginUser(APIView):
    # permission_classes = (partial(MyPermission, ['GET', 'POST', 'HEAD']),)
    def post(self, request):
        try:
            data = request.data
            serializer = LoginSerializer(data=request.data)
            print(data['email'],"--------------")
            user, created = get_user_model().objects.get_or_create(email=data['email'])
            sendOTP(user)
            return Response({
            'status': 200,
            'message': 'Verification code sent on the mail address. Please check',
            # 'data': serializer.data,
            })
        except: 
            return Response({
            'status': 400,
            'message': 'Something went wrong',
            })


class VerifyOTP(APIView):
    # permission_classes = (partial(MyPermission, ['GET', 'POST', 'HEAD']),)
    def post(self, request):
        try:
            data = request.data
            serializer = VerifyUserOTPSerializer(data = data)
            if serializer.is_valid():
                email = serializer.data['email']
                otp = serializer.data['otp']
                try:
                    user = User.objects.get(email=email)
                    if user.otp != otp:
                        return Response({
                            'success': False,
                            'message': 'Invalid OTP. Please enter corrent OTP',  
                        })
                    else:
                        if not user.is_verified:
                            user.is_verified = True
                            user.save()
                            privat_key_gen = make_password(user.email + str(user.id))
                            
                
                            profile , created = UserProfile.objects.get_or_create(user = user, private_key=privat_key_gen, public_key=random_with_N_digits(12))
                            profile.save()
                        user_profile = UserProfile.objects.get(user__email=user)
                        profile_serializer = UserProfileSerializer(user_profile)
                        user = User.objects.get(email = serializer.data['email'])
                        refresh = RefreshToken.for_user(user)
                        return Response({
                                'success': True,
                                'access': str(refresh.access_token),
                                'data': profile_serializer.data
                            })
                except:
                    return Response({
                        'success': False,
                        'message': 'Email not found. Please enter the correct Email Address',
                        
                    })

            return Response({
                        'success': False,
                        'payload': 'Something Went Wrong1',
                        
                    })
        except:
            return Response({
                        'success': False,
                        'message': 'Something Went Wrong',
                    })
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user):
        try: 
            user_profile = UserProfile.objects.get(user__email=user)
            profile_serializer = UserProfileSerializer(user_profile)
            return Response({'success': True, 'payload': profile_serializer.data})
        except:
            return Response({'success': False, 'message': 'Unauthenticted User'})

 
    def put(self, request, user):
        try:
            user_profile = UserProfile.objects.get(user__email=user)
            serializer = UserProfileSerializer(user_profile, data = request.data)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'success': False, 'payload': serializer.errors, 'message': 'Something went wrong'})

            serializer.save()
            return Response({'success': True, 'payload': serializer.data, 'message': 'You have successfully updated..'})

        except Exception as e:
            print(e)
            return Response({'success': False, 'message': 'Invalid ID'})

    def patch(self, request, user):
        try:
            user_profile = UserProfile.objects.get(user__email=user)
            serializer = UserProfileSerializer(user_profile, data = request.data, partial=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response({'success': False, 'payload': serializer.errors, 'message': 'Something went wrong'})

            serializer.save()
            return Response({'success': True, 'payload': serializer.data, 'message': 'You have successfully updated profile.'})

        except Exception as e:
            print(e)
            return Response({'success': False, 'message': 'Invalid ID'})