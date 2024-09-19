from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Project,Category
from .pagination import ProjectPagination
from .serializers import ProjectSerializer,CategorySerializer
from user.permission import IsClientOrReadOnly
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination
    permission_classes = [IsClientOrReadOnly]  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category'] 
    ordering_fields = ['budget'] 

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.clientprofile)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsClientOrReadOnly] 

    def perform_update(self, serializer):
        if self.request.user.clientprofile == serializer.instance.client:
            serializer.save()
        else:
            raise permissions.PermissionDenied("You do not have permission to edit this project.")

    def perform_destroy(self, instance):
        if self.request.user.clientprofile == instance.client:
            instance.delete()
        else:
            raise permissions.PermissionDenied("You do not have permission to delete this project.")

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []  

class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'  
    permission_classes = []  