from rest_framework import serializers
from .models import Proposal
from user.models import FreelancerProfile
from project.models import Project

class ProposalSerializer(serializers.ModelSerializer):
    freelancer = serializers.PrimaryKeyRelatedField(queryset=FreelancerProfile.objects.all())
    project = serializers.SlugRelatedField(slug_field='title', queryset=Project.objects.all())

    class Meta:
        model = Proposal
        fields = '__all__'

    def validate_freelancer(self, value):
        if not isinstance(value, FreelancerProfile):
            raise serializers.ValidationError("The freelancer must be a valid freelancer profile.")
        return value