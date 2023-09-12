from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . serializers import UserRegistrationSerializers,UserLoginSerializer
from . models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . renderers import UserRenderer

#generate token manually
def get_token_for_users(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh':str(refresh),
        'access':str(refresh.access_token),
    }
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    def post(self,request,format=None):
        serializer = UserRegistrationSerializers(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(
                username = serializer.validated_data['username'],
                email = serializer.validated_data['email'],
                password = serializer.validated_data['password'],
            )
            return Response({"Message":"Registration Complete","User":serializer.data},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self,request,format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None:
                token = get_token_for_users(user)
                return Response({"Message":"User Logged Successfully","token":token},status=status.HTTP_200_OK)
            return Response({"Message":"Login Error","errors":{"non_fields_errors":['Email/Password is not valid']}},status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)