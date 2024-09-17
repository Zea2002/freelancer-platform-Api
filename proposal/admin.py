from django.contrib import admin
from .import models
# Register your models here.
class ProposalModelAdmin(admin.ModelAdmin):
    list_display=['title','Freelancer','proposal_status']
    def Freelancer(self,obj):
        return obj.freelancer.user.first_name
    
    def title(self,obj):
        return obj.project.title
    
admin.site.register(models.Proposal,ProposalModelAdmin)