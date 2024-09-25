from rest_framework import viewsets, permissions
from .models import Proposal
from .serializers import ProposalSerializer
from user.permission import IsFreelancer
from .pagination import ProposalPagination
from rest_framework import serializers

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    pagination_class = ProposalPagination
    # permission_classes=[IsFreelancer]

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'freelancer_profile'):
            freelancer_profile = self.request.user.freelancer_profile
            serializer.save(freelancer=freelancer_profile)
        else:
            raise serializers.ValidationError("User is not a freelancer.")
    
    def get_queryset(self):
        queryset = Proposal.objects.all()

        freelancer_id = self.request.query_params.get('freelancer', None)
        project_id = self.request.query_params.get('project', None)
        status = self.request.query_params.get('status', None)

        if freelancer_id:
            queryset = queryset.filter(freelancer_id=freelancer_id)
        if project_id:
            queryset = queryset.filter(project_id=project_id)
        if status:
            queryset = queryset.filter(status=status)

        if self.request.user.is_authenticated and hasattr(self.request.user, 'freelancer_profile'):
            queryset = queryset.filter(freelancer=self.request.user.freelancer_profile)

        return queryset
