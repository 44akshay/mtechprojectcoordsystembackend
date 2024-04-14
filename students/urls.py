from django.urls import path
from . import views

urlpatterns = [
    path('upload',views.upload_file,name='upload_file'),
    path('projectdetails',views.post_project_name,name='post_proj'),
    path('committeedetails',views.comminfo,name='comminfo'),
    path('',views.get_student_project_info,name='students'),

]