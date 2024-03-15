from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportMixin
# Register your models here.

from .models import Faculty

class FacultyResource(resources.ModelResource):
    class Meta:
        model = Faculty
        fields = ('name', 'dept', 'isguide', 'ischair', 'iscommem', 'isprojcoo', 'email', 'domain')
        import_id_fields = ('email',)

class FacAdmin(ImportMixin,admin.ModelAdmin):
    resource_class = FacultyResource
    list_display = ['name', 'dept', 'isguide', 'ischair', 'iscommem', 'isprojcoo', 'email', 'domain']
    search_fields = ['name', 'dept', 'email']  # Enable searching by these fields
    list_filter = ['dept', 'isguide', 'ischair', 'iscommem', 'isprojcoo']  # Add filters for these fields
    actions = ['delete_selected_faculties']

    def delete_selected_faculties(self, request, queryset):
        queryset.delete()

    delete_selected_faculties.short_description = "Delete selected faculties"

admin.site.register(Faculty,FacAdmin)