from django.contrib import admin
from .import models
# Register your models here.
class ProjectModelAdmin(admin.ModelAdmin):
    list_display=['title','Client','budget','category','deadline']
    def Client(self,obj):
        return obj.client.user.first_name
    
class CategoryModelAdmin(admin.ModelAdmin):
    list_display=['name']
    prepopulated_fields = {"slug": ("name",)}




admin.site.register(models.Category,CategoryModelAdmin),
admin.site.register(models.Project,ProjectModelAdmin)