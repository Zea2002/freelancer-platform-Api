from rest_framework import serializers
from .import models
from user.models import ClientProfile


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='user__username', queryset=ClientProfile.objects.all())   
    category = serializers.SlugRelatedField(slug_field='name', queryset=models.Category.objects.all())    

    class Meta:
        model = models.Project
        fields = '__all__'

