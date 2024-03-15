from django.contrib import admin

# Register your models here.

from .models import Project, Limits


class ProjectAdmin(admin.ModelAdmin):
    pass

class LimitsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False
    pass


admin.site.register(Project,ProjectAdmin)
admin.site.register(Limits,LimitsAdmin)
