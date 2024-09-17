from rest_framework import serializers
from .import models

class ProposalSerializer(serializers.ModelSerializer):
    freelancer = serializers.ReadOnlyField(source='freelancer.user.username')
    project = serializers.ReadOnlyField(source='project.title')

    class Meta:
        model = models.Proposal
        fields = '__all__'