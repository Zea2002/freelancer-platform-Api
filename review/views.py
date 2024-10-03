from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Review
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ReviewSerializer
from rest_framework.filters import OrderingFilter
from project.models import Project
from proposal.models import Proposal
from user.permission import IsClientOrReadOnly,IsClient

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsClientOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['freelancer'] 

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Review.objects.filter(project__id=project_id)
        return Review.objects.all()

   