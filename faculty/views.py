from django.shortcuts import render
import json
from django.conf import settings

from django.http import HttpResponse
from django.contrib import messages
#from .forms import ExcelUploadForm
from .models import *
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from  students.models import *
from projects.models import*
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
import re
from .serializers import *
import smtplib
from django.core.mail import send_mail


def addfaculty(request):
     #Creating a faculty object

     facobj=Faculty(name="prof5",dept="CSE", isguide=1,ischair=0 , iscommem=0,isprojcoo=1,email = "dbmsproject019@gmail.com",domain="CV")
     facobj.save()
     return render(request,'home.html',{'facobj':facobj})

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def viewfacs(request):
     #facobj=[]
     #facobj1=[]
     #for i in Faculty.objects.all():
      #    print(i.name)
       #   facobj.append(i.name)
    faculty_objects = Faculty.objects.all()
    faculty_serializer = FacultySerializer(faculty_objects, many=True)
    faculty_json = faculty_serializer.data
    return Response({'faculty': faculty_json})
    # return Response({"facultynames":facobj})


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def addmystudent(request):
    if request.method == "POST":
          print("Test")
          print(request.user.username)
          user = User.objects.get(username = request.user.username)
          #faculty_instance = Faculty.objects.get(email="pg1@nitc.ac.in")
          faculty_instance = Faculty.objects.get(email=request.user.username)
          json_data = json.loads(request.body.decode('utf-8'))
          rollno = json_data.get("rollno")  # Retrieve rollno from JSON data
          sugch=json_data.get("sugchair")
          sugmem1=json_data.get("sugmem1")
          sugmem2=json_data.get("sugmem2")
          print("Rollno received is :", rollno)
          
          student_instance=Project.objects.get(rollNoId=rollno)
          student_instance.guide=faculty_instance
          student_instance.sugg_chair=sugch
          student_instance.sugg_mem1=sugmem1
          student_instance.sugg_mem2=sugmem2
          print("guide::",student_instance.guide.name)
          student_instance.save(update_fields=['guide','sugg_chair','sugg_mem1','sugg_mem2'])
    return Response({'message':'succes'},status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def sendmailto(request):
     print("begin")
    
     print("end")
     #s.login("request.user.username", "request.user.password")
     #s.sendmail("dbmsproject019@gmail.com", "pradnya_m230809cs@nitc.ac.in", message)
     fullmsg=""
     json_data = json.loads(request.body.decode('utf-8'))
     SUBJECT = "Mtech Project Coordination"
     rollno=json_data.get("rollno")
     date=json_data.get("date")
     time=json_data.get("time")
     loc=json_data.get("loc")
     desc=json_data.get("desc")
     invite=json_data.get("invite")
     fullmsg+="Roll No: "+rollno+"\n"+"Date: "+date+"\n"+"Time: "+time+"\n"+"Location: "+loc+"\n"+"Description: "+desc+"\n"+"Invite: "+invite+"\n"
     print(fullmsg)
     message = 'Subject: {}\n\n{}'.format(SUBJECT,fullmsg )
     print("rec")
     a=[]
     a.append(request.user.username)

     rec=Project.objects.get(rollNoId =rollno).chair_person.email
     a.append(rec)
     print(rec)
     #s = smtplib.SMTP('smtp.gmail.com', 587)
# start TLS for security
    # s.starttls()
     #s.login("dbmsproject019@gmail.com", "cfsf ctnp lnpp wmjg")

     #s.sendmail("dbmsproject019@gmail.com", "dbmsproject019@gmail.com", message)

     for i in Project.objects.get(rollNoId =rollno).committee_members.all():
          print(i.email)
          a.append(i.email)
    # b=Project.objects.get(rollNoId =rollno)
     
     #i=b.committee_members.all()
     #print(i.email)  
         #s.sendmail(request.user.username, i.email, message)
     #s.quit()
     print("after rec")
     print(a)
     from_email = settings.EMAIL_HOST_USER
     send_mail(SUBJECT, fullmsg, from_email,a )
     return Response({'message':'succes'},status=200)

