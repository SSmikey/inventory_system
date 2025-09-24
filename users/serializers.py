from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name', 'last_name', 'role']
        extra_kwargs = {
            'role': {'default': 'staff'}  # ถ้าไม่ส่ง role จะใช้ staff
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            role=validated_data.get('role', 'staff')  # 👈 รองรับ role
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # เพิ่มข้อมูล role ลงไปใน token
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # เพิ่มข้อมูล role ใน response
        data['role'] = self.user.role
        data['username'] = self.user.username
        return data

    def create(self, validated_data):
        # Not used, but required to satisfy abstract methods
        pass

    def update(self, instance, validated_data):
        # Not used, but required to satisfy abstract methods
        pass
