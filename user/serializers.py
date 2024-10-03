from rest_framework import serializers
from .models import FreelancerProfile, Skill, ClientProfile,User
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True)  
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True) 
    user_display = serializers.StringRelatedField(source='user', read_only=True) 

    class Meta:
        model = FreelancerProfile
        fields = '__all__' 

    def create(self, validated_data):
        skills_data = validated_data.pop('skills') 
        user = validated_data.pop('user')  

       
        freelancer_profile = FreelancerProfile.objects.create(user=user, **validated_data)

class ClientProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  
    user_display = serializers.StringRelatedField(source='user', read_only=True)

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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type', 'first_name', 'last_name']

class UserLoginSerializer(serializers.Serializer):
    username= serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
