from django.urls import path,include
from .views import CategoryViewSet,ProjectViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'projects', ProjectViewSet)
urlpatterns = [
    path('', include(router.urls)),
]

