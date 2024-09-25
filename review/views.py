from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewSerializer
from project.models import Project
from proposal.models import Proposal
from user.permission import IsClientOrReadOnly,IsClient

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsClientOrReadOnly]

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsClient]
        return super().get_permissions()

    def get_queryset(self):
        project_id = self.request.query_params.get('project')
        if project_id:
            return Review.objects.filter(project__id=project_id)
        return Review.objects.all()

    def perform_create(self, serializer):
        project_id = self.request.data.get('project')
        freelancer_id = self.request.data.get('freelancer')

        project = Project.objects.get(id=project_id)

        if project.client != self.request.user.client_profile:
            raise ValidationError("You can only review projects you have commissioned.")

        try:
            proposal = Proposal.objects.get(project=project, freelancer__id=freelancer_id)
        except Proposal.DoesNotExist:
            raise ValidationError("No matching proposal found for this freelancer and project.")

        if proposal.proposal_status != 'Completed':
            raise ValidationError("You cannot review a project that is not completed.")

        serializer.save(reviewer=self.request.user.client_profile, project=project, freelancer=proposal.freelancer)
