from rest_framework import serializers
from .import models
from user.models import FreelancerProfile, ClientProfile
from project.models import Project

class ReviewSerializer(serializers.ModelSerializer):
    freelancer = serializers.SlugRelatedField(slug_field='user__username', queryset=FreelancerProfile.objects.all())
    project = serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())
    reviewer = serializers.SlugRelatedField(slug_field='user__username', queryset=ClientProfile.objects.all())
    
    class Meta:
        model = models.Review
        fields = '__all__'
