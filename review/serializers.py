from rest_framework import serializers
from .import models

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.user.username')
    freelancer = serializers.ReadOnlyField(source='freelancer.user.username')
    project = serializers.ReadOnlyField(source='project.title')
    class Meta:
        model = models.Review
        fields = '__all__'