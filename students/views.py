from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Student
from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from projects.models import Project
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from mtech_pc_system.serializers import ProjectSerializer
import json

def students(request):

    return HttpResponse("Hello World!!!")

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_student_project_info(request):
    print(request.user.username)
    # Retrieve the student instance based on the user (assuming user authentication is already handled)
    student_user = get_object_or_404(Student,email = request.user.email)
    project = Project.objects.get(student=student_user)
    # Check if isGuideSelected is True
    print(project.guide)
    
    if project.guide:
        if project.projectname != "Default":
            serializer = ProjectSerializer(instance=project)
            return Response({"project":serializer.data,"isGuideSelected":"True","isProjectUploaded":"True"},status=200)
        else:
            return Response({"project":serializer.data,"isGuideSelected":"True","isProjectUploaded":'False'}, status=400)
    else:
        return Response({"isGuideSelected":"False"}, status=400)
