from django.db import models
from user.models import FreelancerProfile,ClientProfile
from project.models import Project
# Create your models here.
STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]    
class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    reviewer=models.ForeignKey(ClientProfile,on_delete=models.CASCADE)
    rating = models.CharField(choices = STAR_CHOICES, max_length = 10)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Client : {self.reviewer.user.first_name} ; Freelancer: {self.freelancer.user.first_name}"