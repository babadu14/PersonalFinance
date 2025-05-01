from rest_framework import serializers
from users.models import EmailVerification
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'first_name', 'last_name')

class RegisterSerielizer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','username','phone_number','password', 'password2','first_name', 'last_name')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"message":"passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_active = False
        user.save()
        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True, required=True)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'email', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)

        instance.save()
        return instance
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = User.objects.get(email=value)
        except:
            raise serializers.ValidationError('user does not exist')
        return value

