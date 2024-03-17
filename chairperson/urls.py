from django.urls import path
from . import views

urlpatterns = [
    path('get_students_chair/',views.get_students_chair,name='get_students_chair'),
    path('givemarks/',views.givemarks,name='givemarks'),

]