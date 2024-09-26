from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.db import models

class User(AbstractUser):
    FREELANCER = 'freelancer'
    CLIENT = 'client'
    
    USER_TYPE_CHOICES = [
        (FREELANCER, 'Freelancer'),
        (CLIENT, 'Client'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=CLIENT)

class Skill(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class FreelancerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='freelancer_profile')
    skills = models.ManyToManyField(Skill, related_name='freelancers')
    profile_pic = models.ImageField(upload_to='user/media/freelancer/', null=True, blank=True)
    portfolio_url = models.URLField(blank=True)
    phone = models.CharField(max_length=12)
    bio = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    location = models.CharField(max_length=30)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client_profile')
    company_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=12)
    profile_pic = models.ImageField(upload_to='user/media/client/', null=True, blank=True)
    company_website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=30)
    is_verified = models.BooleanField(default=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
