from django.urls import path
from . import views

urlpatterns = [
    path('showfac/',views.addfaculty,name='addfaculty'),
        path('addmystudent/',views.addmystudent,name='addmystudent'),
    path('viewfacs/',views.viewfacs,name='viewfacs'),
        path('sendmailto/',views.sendmailto,name='sendmailto'),

    path('viewAllStud/',views.getAllStudents,name='sendmailto'),

]