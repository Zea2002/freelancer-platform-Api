from django.urls import path
from .views import ProjectListView, ProjectDetailView,CategoryListView,CategoryDetailView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'), 
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),  
]
