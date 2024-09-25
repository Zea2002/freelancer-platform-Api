from rest_framework import serializers
from .models import FreelancerProfile, Skill, ClientProfile
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = FreelancerProfile
        fields = '__all__'

class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = ClientProfile
        fields = '__all__'

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password','confirm_password', 'user_type']

   
    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password=self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        user_type=self.validated_data['user_type']

        if password != password2:
             raise serializers.ValidationError({'error' : "Password Doesn't match"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        account = User(username = username, email=email,user_type=user_type,first_name = first_name, last_name = last_name)
        account.set_password(password)
        account.save()
        return account



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if user is None:
                raise serializers.ValidationError(_('Invalid email or password'))
            if not user.is_active:
                raise serializers.ValidationError(_('User account is disabled.'))

        else:
            raise serializers.ValidationError(_('Both "email" and "password" are required.'))

        data['user'] = user
        return data


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
