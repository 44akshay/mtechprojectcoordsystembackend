from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Student
from faculty.models import Faculty
import os
from django.http import JsonResponse,FileResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from projects.models import Project,Domain,Limits
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from mtech_pc_system.serializers import ProjectSerializer,getRollNoSerializer,LimitSerializer
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
def project_details(request):
    studentRollNo = request.data["rollNoId"]
    #print(studentRollNo)
    student = get_object_or_404(Student,rollNoId = studentRollNo)
    project = Project.objects.get(student = student)
    serializer = ProjectSerializer(instance=project)
    print(serializer.data)
    # print("project obj",project.Phase1.Report)
    # report_file=project.Phase1.Report
    # # print(report_file)
    # serializer.data.Phase1.Report = True

    # if not report_file:
    #     serializer.data.Phase1.Report = False
    
    # report_file=project.Phase2.Report
    # # print(report_file)
    # project.Phase2.Report = True

    # if not report_file:
    #     serializer.data.Phase2.Report = False
    
    # report_file=project.Phase3.Report
    # # print(report_file)
    # project.Phase3.Report = True
    # if not report_file:
    #     serializer.data.Phase3.Report = False
    limit_object = Limits.objects.get(Limit="Limit")
    limit_serializer = LimitSerializer(limit_object)
    limit_serializer_data = limit_serializer.data
    return Response({"projectdata":serializer.data,"limit":limit_serializer_data},status=200)

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def send_project_reports(request):
    studentRollNo = request.data["rollNoId"]
    phase  = request.data["phase"]
    print(studentRollNo)
    student = get_object_or_404(Student,rollNoId = studentRollNo)
    project = Project.objects.get(student = student)
    # serializer = ProjectSerializer(instance=project)
    print("project obj",project.Phase1.Report)
    if phase == "1":
        
        report_file=project.Phase1.Report
    elif phase == "2":
        report_file=project.Phase2.Report
    else:
        report_file=project.Phase3.Report


    print(report_file)
    if not report_file:
        return Response({"error": "Report file not found"}, status=404)
    report_file_path = report_file.path  # Get the file path from the FieldFile object
    # serializer = ProjectSerializer(instance=project)
    # project_data = serializer.data
    try:
        # Check if the file path exists
        if os.path.exists(report_file_path):
            # Open the file in binary mode for reading
            with open(report_file_path, 'rb') as report_file:
                # Read the file content
                file_content = report_file.read()

            # Create an HttpResponse object with the file content as attachment
            response = HttpResponse(file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_file_path)}"'
            
            # Return the response with the file as attachment
            return response
        else:
            return Response({"error": "File not found"}, status=200)

    except Exception as e:
        return Response({"error": str(e)}, status=500)

# @api_view(['POST'])
# @authentication_classes([SessionAuthentication,TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def send_project_reports(request):
#     studentRollNo = request.data["rollNoId"]
#     print(studentRollNo)
#     student = get_object_or_404(Student,rollNoId = studentRollNo)
#     project = Project.objects.get(student = student)
#     serializer = ProjectSerializer(instance=project)


#     # Projects_under_guide = faculty_guide.guide_projects.all()
#     # data = getRollNoSerializer(Projects_under_guide,many=True)
#     project_data = serializer.data
#     return JsonResponse({'project_data':project_data},status=200)

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