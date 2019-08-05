from django.contrib import admin

# Register your models here.
from core.models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'deadline', 'approved_by_admin')
    readonly_fields = ('name', 'deadline', 'picture')

    def get_queryset(self, request):
        return self.model.admin_manager.get_queryset()


admin.site.register(Project, ProjectAdmin)
