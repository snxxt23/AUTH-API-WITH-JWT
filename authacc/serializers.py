from rest_framework import serializers
from . models import *
import re

class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    #validating password and confirm password while registration
    def validate(self,data):
        password = data.get('password')
        password2 = data.get('password2')
        username = data.get('username')
        if password != password2:
            raise serializers.ValidationError('Passwords Mismatching')
        elif re.match(r"^\d{1,3}",username):
            raise serializers.ValidationError('Username should starts with Alphabets')
        return data

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ['email','password']