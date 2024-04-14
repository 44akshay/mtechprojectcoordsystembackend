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
from projects.models import Project,Domain,Limits
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from mtech_pc_system.serializers import ProjectSerializer,DomainSerializer,LimitSerializer
import json

# import faculty.models import Faculty


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
    domain_objects= Domain.objects.all()
    domain_serializer = DomainSerializer(domain_objects, many=True)
    domain_serializer_data = domain_serializer.data
    #print(project.guide)
    print(domain_serializer_data)
    limit_object = Limits.objects.get(Limit="Limit")
    limit_serializer = LimitSerializer(limit_object)
    limit_serializer_data = limit_serializer.data

    
    if project.guide:
        if project.projectname != "Default":
            serializer = ProjectSerializer(instance=project)
            return Response({"project":serializer.data,"isGuideSelected":"True","isProjectUploaded":"True","domain":domain_serializer_data,"limit":limit_serializer_data},status=200)
        else:
            serializer = ProjectSerializer(instance=project)
            return Response({"project":serializer.data,"isGuideSelected":"True","isProjectUploaded":'False',"domain":domain_serializer_data}, status=200)
    else:
        return Response({"isGuideSelected":"False"}, status=200)


@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def post_project_name(request):
    print(request.user.username)
    # Retrieve the student instance based on the user (assuming user authentication is already handled)
    student_user = get_object_or_404(Student,email = request.user.email)
    project = Project.objects.get(student=student_user)
    # Check if isGuideSelected is True
    # domain = Domain.object.
    data = json.loads(request.body)
    domain_array = data.get('domains', [])
    projectname = data.get('projectname')

    if projectname:
        project.projectname = projectname
        project.save(update_fields=['projectname'])
    for domain_name in domain_array:
        domain_obj, created = Domain.objects.get_or_create(domain_name=domain_name)
        project.domain_categories.add(domain_obj)


    project1= Project.objects.get(student=student_user)
    # print(project1)
    # print(project1.domain_categories.all())
    return JsonResponse({'Success':'200'},status=200)


StatusChoices = (
        (0, 'Pending'),
        (1, 'Rejected'),
        (2, 'Accepted'),
        (3, 'UnderReview'),


    )

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_file(request):
    print("hello")
    print(type(request.POST['phase']))
    phase = request.POST['phase']
    file = request.FILES['file']

    if not request.FILES.get('file'):
        return JsonResponse({'error': 'File not provided or invalid method'}, status=400)

    student_user = get_object_or_404(Student,email = request.user.email)
    project = Project.objects.get(student=student_user)

    if phase == "1":
        phase1 = project.Phase1
        phase1.Report = file
        phase1.Status = StatusChoices[3][1]

        phase1.save(update_fields= ['Report','Status'])
        
        project.save(update_fields= ['Phase1'])
       # project.Phase1.Report =  file
    elif phase == "2":
        phase2 = project.Phase2
        phase2.Report = file
        phase2.Status = StatusChoices[3][1]
        phase2.save(update_fields= ['Report','Status'])
        project.save(update_fields= ['Phase2'])
    elif phase == "3":
        phase3 = project.Phase3
        phase3.Report = file
        phase3.Status = StatusChoices[3][1]

        phase3.save(update_fields= ['Report','Status'])

        project.save(update_fields= ['Phase3'])

    project = Project.objects.get(student=student_user)

    print(project.Phase1.Status)
    return JsonResponse({'file_name': file.name},status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def comminfo(request):
    stud=Student.objects.get(email=request.user.username)
    proj=Project.objects.get(student=stud)
    if proj.guide is not None:
        guideName=proj.guide.name
        print(proj.guide.name)
    else:
        guideName="Not Allocated"
    if proj.chair_person is not None:
        chairperson=proj.chair_person.name
        print(proj.chair_person.name)
    else:
        chairperson="Not Allocated"
    committeeMember1="Not Allocated"
    committeeMember2="Not Allocated"
    j=0
    for i in proj.committee_members.all():
        if(j==0):
            committeeMember1=i.name
            j+=1
        elif(j==1):
            committeeMember2=i.name
    response_data = {
    "guideName": guideName,
    "chairperson": chairperson,
    "committeeMember1": committeeMember1,
    "committeeMember2": committeeMember2,
    }
    json_response = json.dumps(response_data)
    print(json_response)
    return JsonResponse(response_data)


