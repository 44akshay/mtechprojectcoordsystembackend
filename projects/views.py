from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Student
from faculty.models import Faculty

from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from projects.models import Project,Domain
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from mtech_pc_system.serializers import ProjectSerializer,getRollNoSerializer
import json

# Create your views here.
@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_students(request):
    faculty_guide = get_object_or_404(Faculty,email = request.user.email)
    Projects_under_guide = faculty_guide.guide_projects.all()
    data = getRollNoSerializer(Projects_under_guide,many=True)
    student_data = data.data
    return JsonResponse({'StudentData':student_data},status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_project_reports(request):
    studentRollNo = request.data["rollNoId"]
    print(studentRollNo)
    student = get_object_or_404(Student,rollNoId = studentRollNo)
    project = Project.objects.get(student = student)
    serializer = ProjectSerializer(instance=project)


    # Projects_under_guide = faculty_guide.guide_projects.all()
    # data = getRollNoSerializer(Projects_under_guide,many=True)
    project_data = serializer.data
    return JsonResponse({'project_data':project_data},status=200)

StatusChoices = (
        (0, 'Pending'),
        (1, 'Do Modify  & Watch Comment'),
        (2, 'Accepted'),
        (3, 'UnderReview'),


    )

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def accept_report(request):
    studentRollNo = request.data["rollNoId"]
    phase = request.data["phase"]
    print(studentRollNo)
    student = get_object_or_404(Student,rollNoId = studentRollNo)
    project = Project.objects.get(student = student)

    if phase == "1":
        phase1 = project.Phase1
        phase1.Status = StatusChoices[2][1]

        phase1.save(update_fields= ['Status'])
        project.save(update_fields= ['Phase1'])
       # project.Phase1.Report =  file
    elif phase == "2":
        phase2 = project.Phase2
        phase2.Status = StatusChoices[2][1]
        phase2.save(update_fields= ['Status'])
        project.save(update_fields= ['Phase2'])
    elif phase == "3":
        phase3 = project.Phase3
        phase3.Status = StatusChoices[2][1]

        phase3.save(update_fields= ['Status'])

        project.save(update_fields= ['Phase3'])

    project1 = Project.objects.get(student=student)

    print(project.Phase1.Status)
    serializer = ProjectSerializer(instance=project1)
    project_data = serializer.data

    return JsonResponse({'message':"success","check":serializer.data},status=200)



@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def modify_comment(request):
    studentRollNo = request.data["rollNoId"]
    phase = request.data["phase"]
    comment = request.data["comment"]

    # print(studentRollNo)
    student = get_object_or_404(Student,rollNoId = studentRollNo)
    project = Project.objects.get(student = student)

    if phase == "1":
        phase1 = project.Phase1
        phase1.Status = StatusChoices[1][1]
        phase1.Report_Comments = comment
        phase1.save(update_fields= ['Status','Report_Comments'])
        project.save(update_fields= ['Phase1'])
       # project.Phase1.Report =  file
    elif phase == "2":
        phase2 = project.Phase2
        phase2.Status = StatusChoices[1][1]
        phase2.Report_Comments = comment
        phase2.save(update_fields= ['Status','Report_Comments'])
        project.save(update_fields= ['Phase2'])
    elif phase == "3":
        phase3 = project.Phase3
        phase3.Status = StatusChoices[1][1]
        phase3.Report_Comments = comment

        phase3.save(update_fields= ['Status','Report_Comments'])

        project.save(update_fields= ['Phase3'])

    project1 = Project.objects.get(student=student)

    print(project.Phase1.Status)
    serializer = ProjectSerializer(instance=project1)
    project_data = serializer.data

    return JsonResponse({'message':"success","check":serializer.data},status=200)