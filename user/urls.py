from django.urls import path
from .views import RegisterView, ActivateView, LoginView, LogoutView, UpdateProfileView, ChangePasswordView, FreelancerProfileListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('freelancers/', FreelancerProfileListView.as_view(), name='freelancer_list'),
]
