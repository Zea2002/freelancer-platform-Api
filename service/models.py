from django.db import models

# Create your models here.
class Service(models.Model):
    title=models.CharField(max_length=20,blank=True)
    img=models.ImageField(upload_to='Service/image/',blank=True)
    description=models.TextField()