from .models import Beeline,Profile
from rest_framework import serializers
from django.contrib.auth.models import User

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile 
        fields = '__all__'


class BeelineSerializer(serializers.ModelSerializer):
    beeline = ProfileSerializer(read_only=True,many=True)
    class Meta:
        model=Beeline
        fields = '__all__'

"""class UploadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Upload
        fields = '__all__'"""


MIN_LENGTH = 8 
class UserSerializer(serializers.ModelSerializer):
    """password = serializers.CharField(
        write_only = True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length":f"password must be longer that {MIN_LENGTH} characters"
        }
    )
    password2 = serializers.CharField(
        write_only = True,
        min_length=MIN_LENGTH,
        error_messages={
            "min_length":f"password must be longer that {MIN_LENGTH} characters"
        }
    )"""
    class Meta:
        model = User 
        fields = "__all__"
    """def validate(self,data):
        if data['password'] !=data['password2']:
            raise serializers.ValidationError("password does not match")
        return data
    def create(self,validated_data):
        user = User.objects.create(
        username=validated_data["username"],
        email = validated_data["email"],
        first_name = validated_data["first_name"],
        last_name = validated_data["last_name"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user"""