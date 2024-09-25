from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
