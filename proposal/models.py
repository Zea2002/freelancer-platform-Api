from django.db import models
from user.models import FreelancerProfile
from project.models import Project

# Create your models here.
PROPOSAL_STATUS = [
    ('Completed', 'Completed'),
    ('Pending', 'Pending'),
    ('Accepted', 'Accepted'),
    ('Rejected', 'Rejected'),
]

class Proposal(models.Model):
    freelancer = models.ForeignKey(FreelancerProfile, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    proposal_status = models.CharField(choices=PROPOSAL_STATUS, max_length=10, default='Pending')
    about_on_project = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Freelancer: {self.freelancer.user.first_name}, Project: {self.project.title}"
    
    class Meta:
        verbose_name_plural = "Proposals"