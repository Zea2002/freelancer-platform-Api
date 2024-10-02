from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project,Category
from .pagination import ProjectPagination
from rest_framework.filters import OrderingFilter
from .serializers import ProjectSerializer,CategorySerializer
from user.permission import IsClientOrReadOnly

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes=[IsClientOrReadOnly]
    pagination_class = ProjectPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    
    
    filterset_fields = ['category','client'] 
    
    
    ordering_fields = ['budget']
    ordering = ['budget']  

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer