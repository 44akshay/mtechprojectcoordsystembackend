from django.shortcuts import render
from django.shortcuts import render
import json
from django.conf import settings

from django.http import HttpResponse
from django.http import JsonResponse

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
from mtech_pc_system.serializers import *

from  faculty.models import *
import json
# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_students_chair(request):
    chair = get_object_or_404(Faculty,email = request.user.email)
    Projects_under_chair = chair.chair_projects.all()
    data = chairpSerializer(Projects_under_chair,many=True)
    student_data = data.data
    print(request.user.email)
    return JsonResponse({'StudentData':student_data},status=200)



@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def givemarks(request):
    if request.method == "POST":
        studentRollNo = request.data["rollNoId"]
        print(studentRollNo)
        print(request.user.username)
        print("Test")
        student = get_object_or_404(Student,rollNoId = studentRollNo)

        student_instance=Project.objects.get(rollNoId=studentRollNo)
         # user = User.objects.get(username = request.user.username)
          #faculty_instance = Faculty.objects.get(email="pg1@nitc.ac.in")
          #json_data = json.loads(request.body.decode('utf-8'))
            # Retrieve rollno from JSON data
        phase=request.data["phase"]
        marks=request.data["marks"]
        comments=request.data["comments"]
        if(phase=='1'):
            phase1 = student_instance.Phase1
            phase1.Evaluation=marks
            phase1.Evaluation_Comments=comments
            phase1.save(update_fields= ['Evaluation','Evaluation_Comments'])
            student_instance.save(update_fields= ['Phase1'])
        if(phase=='2'):
            phase2 = student_instance.Phase2
            phase2.Evaluation=marks
            phase2.Evaluation_Comments=comments
            phase2.save(update_fields= ['Evaluation','Evaluation_Comments'])
            student_instance.save(update_fields= ['Phase2'])
        elif(phase=='3'):
            phase3 = student_instance.Phase3
            phase3.Evaluation=marks
            phase3.Evaluation_Comments=comments
            phase3.save(update_fields= ['Evaluation','Evaluation_Comments'])
            student_instance.save(update_fields= ['Phase3'])
        project1 = Project.objects.get(student=student)
        print(student_instance.Phase2.Evaluation)
        serializer = ProjectSerializer1(instance=project1)
        project_data = serializer.data
        return Response({'message':'succes',"check":serializer.data},status=200)

# @api_view(['POST'])
# @authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def get_students_chair(request):
#     chair = get_object_or_404(Faculty,email = request.user.email)
#     Projects_under_chair = chair.chair_projects.all()
#     data = chairpSerializer(Projects_under_chair,many=True)
#     student_data = data.data
#     print(request.user.email)
#     return JsonResponse({'StudentData':student_data},status=200)
@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def project_details(request):
    studentRollNo = request.data["rollNoId"]
    #print(studentRollNo)
    student = get_object_or_404(Student,rollNoId = studentRollNo)
    project = Project.objects.get(student = student)
    serializer = ProjectSerializer(instance=project)
    limit_object = Limits.objects.get(Limit="Limit")
    limit_serializer = LimitSerializer(limit_object)
    limit_serializer_data = limit_serializer.data
    print(serializer.data)
   

    return Response({"projectdata":serializer.data,"limit":limit_serializer_data},status=200)