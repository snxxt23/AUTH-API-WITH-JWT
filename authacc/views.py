from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from . serializers import UserRegistrationSerializers,UserLoginSerializer,UserProfileSerializer,AllUsersSerializer
from . models import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from . renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.decorators import api_view

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
    renderer_classes = [UserRenderer]
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

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserProfileEdit(APIView):
    serializer_classes = [UserProfileSerializer]
    permission_classes = [IsAuthenticated]
    # permission_classes = [IsAdminUser]
    renderer_classes = [UserRenderer]
    filter_backends = [SearchFilter]
    search_fields = ['^name','=email']

    def get(self,request,pk=None):
        if pk is not None:
            user = User.objects.get(id=pk)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response({"Message":"GET method is not allowed here.!!!"})
    
    def put(self,request,pk=None):
        if pk is not None:
            user = User.objects.get(pk=pk)
            serializer = UserProfileSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"Message":"Profile Updated","Profile":serializer.data},status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message":"Select a user"})
    
    def delete(self,request,pk=None):
        if pk is not None:
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({"Message":"User Doesn't Exist.!!!"},status=status.HTTP_400_BAD_REQUEST)
            user.delete()
            return Response({"Message":"User Deleted.!!!"},status=status.HTTP_200_OK)
        return Response({"Message":"Select a User"})

    @api_view(['GET','POST','PUT','PATCH','DELETE'])
    def url_check(request,*args,**kwargs):
        return Response({"Error":"Invalid URL pattern"},status=status.HTTP_404_NOT_FOUND)

class AllUsers(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        user = User.objects.all()
        serializer = AllUsersSerializer(user,many=True)
        return Response(serializer.data)