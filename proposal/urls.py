from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProposalViewSet, AppliedJobHistoryView

router = DefaultRouter()
router.register(r'proposals', ProposalViewSet, basename='proposal')

urlpatterns = [
    path('', include(router.urls)),
    path('applied-jobs/', AppliedJobHistoryView.as_view(), name='applied-job-history'),
]
