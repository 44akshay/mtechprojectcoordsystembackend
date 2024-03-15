from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
#from .forms import ExcelUploadForm
from .models import *
# 
def addfaculty(request):
     #Creating a faculty object
     facobj=faculty(name="ABC",dept="CSE", isguide=1,ischair=2 , iscommem=3,isprojcoo=1,email = "abc@gmail.com",domain="CV")
     facobj.save()
     return render(request,'home.html',{'facobj':facobj})


