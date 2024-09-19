from rest_framework import serializers
from .import models
class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.username')
    category = serializers.StringRelatedField()
    class Meta:
        model = models.Project
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields ='__all__'