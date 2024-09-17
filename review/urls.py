from django.urls import path
from .views import ReviewCreateView, ReviewListView

urlpatterns = [
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),
    path('', ReviewListView.as_view(), name='review-list'),
]
