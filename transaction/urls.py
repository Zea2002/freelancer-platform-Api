
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = [
    # Other URLs
    path('', include(router.urls)),
]
