from django.contrib import admin
from .import models
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')

class ClientModelAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','profile_pic','phone']
    
    def first_name(self,obj):
        return obj.user.first_name
    
    def last_name(self,obj):
        return obj.user.last_name

class FreelancerModelAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','profile_pic','phone']
    filter_horizontal = ('skills',)
    
    def first_name(self,obj):
        return obj.user.first_name
    
    def last_name(self,obj):
        return obj.user.last_name

class SkillModelAdmin(admin.ModelAdmin):
    list_display=['name']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(models.FreelancerProfile,FreelancerModelAdmin)
admin.site.register(models.ClientProfile,ClientModelAdmin)
admin.site.register(models.Skill,SkillModelAdmin)
admin.site.register(models.User,UserAdmin)

