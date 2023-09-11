from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . serializers import UserRegistrationSerializers
from . models import *

class UserRegistrationView(APIView):
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