from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Project
from .pagination import ProjectPagination
from .serializers import ProjectSerializer
from user.permission import IsClient
class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = ProjectPagination
    permission_classes = [IsAuthenticatedOrReadOnly,IsClient]  
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category'] 
    ordering_fields = ['budget'] 

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.clientprofile)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsClient] 

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
