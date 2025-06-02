from rest_framework import serializers
from users.models import EmailVerification
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


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

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid64 = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, required=True, validators = [validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"message":"password do nto match"})
        
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid64"]))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            raise serializers.ValidationError({"message":"მომხმარებელი ვერ მოიძებნა"})
        
        token = attrs["token"]
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"message":"incorrect or expired token"})
        
        attrs["user"] = user
        return attrs
    
    def save(self):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()

class EmailCodeResendSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"message":"user was not found"})
        attrs['user'] = user
        return attrs
    
class EmailCodeConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        code = attrs.get("code")

        try:
            user = User.objects.get(email=email)
            verification = EmailVerification.objects.filter(user=user).first()
            if not verification.code == code:
                raise serializers.ValidationError({"message":"code is incorrect"})
            
            if verification.is_expired():
                raise serializers.ValidationError({"message":"code is expired"})
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            raise serializers.ValidationError({"message":"user or the code is incorrect"})
        
        attrs['user'] = user
        return attrs