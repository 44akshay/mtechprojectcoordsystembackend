from django.urls import path
from . import views

urlpatterns = [


    path('getStudents/',views.getAllStudents,name='getStudents'),
    path('getAvailInfo/',views.getStudentDataAndAvail,name='Info'),
    path('setCommittee/',views.setCommittee,name='setCommittee'),
    path('evaluate/',views.ViewAllEvaluations,name='evaluate'),

    # path('',include)

]