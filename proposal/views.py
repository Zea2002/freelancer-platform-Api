from rest_framework import viewsets,permissions,generics
from .models import  Proposal
from .serializers import ProposalSerializer
from user.permission import IsFreelancer
from .pagination import ProposalPagination

# Create your views here.
class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    

    def get_permissions(self):
        if self.action == 'create':
            return [IsFreelancer()]
        return [permissions.IsAuthenticated()]
    
    
class AppliedJobHistoryView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    pagination_class = ProposalPagination

    def get_queryset(self):
        return Proposal.objects.filter(freelancer=self.request.user)
    
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

        return queryset