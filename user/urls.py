from django.urls import path,include
from .views import RegisterView, activate, LoginView, LogoutView, UpdateProfileView, ChangePasswordView,SkillViewSet,FreelancerProfileViewSet,ClientProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'freelancers', FreelancerProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'client', ClientProfileViewSet)
urlpatterns = [
    path('', include(router.urls)),
  path('register/', RegisterView.as_view(), name='register'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]

