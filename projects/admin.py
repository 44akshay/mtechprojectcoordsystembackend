from django.contrib import admin

# Register your models here.

from .models import Project, Limits,Domain,Phase


class ProjectAdmin(admin.ModelAdmin):
    pass

class LimitsAdmin(admin.ModelAdmin):
    # def has_add_permission(self, request):
    #     return False
    pass

class DomainAdmin(admin.ModelAdmin):
    pass

class PhaseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project,ProjectAdmin)
admin.site.register(Limits,LimitsAdmin)
admin.site.register(Domain,DomainAdmin)
admin.site.register(Phase,PhaseAdmin)


