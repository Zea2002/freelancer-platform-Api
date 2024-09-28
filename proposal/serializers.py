from rest_framework import serializers
from .models import Proposal
from user.models import FreelancerProfile
from project.models import Project

class ProposalSerializer(serializers.ModelSerializer):
    freelancer = serializers.SlugRelatedField(slug_field='user__username', queryset=FreelancerProfile.objects.all())
    project= serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())
    class Meta:
        model = Proposal
        fields = '__all__'
