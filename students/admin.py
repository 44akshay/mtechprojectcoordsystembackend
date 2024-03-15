from import_export import resources, fields
from import_export.admin import ImportMixin
from django.contrib import admin
from .models import Student
from django.contrib.auth.models import User
from projects.models import Project



class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = ('firstname', 'lastname', 'rollNoId', 'email', 'semester', 'program', 'isGuideSelected', 'created_at', 'updated_at', 'project_name')
        import_id_fields = ('rollNoId', )

class StudentAdmin(ImportMixin, admin.ModelAdmin):
    resource_class = StudentResource
    list_display = ['firstname', 'lastname', 'rollNoId', 'email', 'semester', 'program', 'isGuideSelected', 'created_at', 'updated_at', 'project_name']
    search_fields = ['firstname', 'lastname', 'rollNoId', 'email']  # Enable searching by these fields
    list_filter = ['semester', 'program', 'isGuideSelected']  # Add filters for these fields
    actions = ['delete_selected_students']

    def delete_selected_students(self, request, queryset):
        queryset.delete()

    delete_selected_students.short_description = "Delete selected students"



admin.site.register(Student, StudentAdmin)
