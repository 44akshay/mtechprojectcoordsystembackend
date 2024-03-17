from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from faculty.models import Faculty

from django.http import JsonResponse
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from projects.models import Project,Domain,Limits
from students.models import Student
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from mtech_pc_system.serializers import StudentSerializer
from faculty.serializers import FacultySerializer
import json
from .serializers import ProjectSerializer


@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def getAllStudents(request):
    student_objects = Student.objects.all()
    student_serializer = StudentSerializer(student_objects, many=True)
    student_data = student_serializer.data
    
   # limit_object = Limits.objects.get(Limit="Limit")
   # Available_chairs = Faculty.objects.get(ischair<limit_object.ChairPerson)
   # Available_Committees = Faculty.objects.get(iscommem<limit_object.CommitteeLimit)




    return Response({'students': student_data})

@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def getStudentDataAndAvail(request):
    rollno = request.data['rollNoId']
    project_instance = Project.objects.get(rollNoId=rollno)

    # student_objects = Student.objects.all()
    # student_serializer = StudentSerializer(student_objects, many=True)
    # student_data = student_serializer.data
    
    limit_object = Limits.objects.get(Limit="Limit")
    Available_chairs = Faculty.objects.filter(ischair__lt =limit_object.ChairPerson)
    Available_committees = Faculty.objects.filter(iscommem__lt =limit_object.CommitteeLimit)
    chair_serializer = FacultySerializer(Available_chairs,many=True)
    committee_serializer = FacultySerializer(Available_committees,many=True)
    if project_instance.chair_person:
        # print(project_instance.chair_person.name)
        isCommittee = True
    else:
        isCommittee = False


    return Response({'chair': chair_serializer.data,'committee':committee_serializer.data,'project_name':project_instance.projectname,'guide_name':project_instance.guide.name,'isCommittee':isCommittee})





@api_view(['POST'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def setCommittee(request):
    rollno = request.data['rollNoId']
    chair = request.data['chairId']
    committee1 = request.data['committee1']
    committee2 = request.data['committee2']

    chair_instance = Faculty.objects.get(email = chair)
    committee1_instance = Faculty.objects.get(email = committee1)
    committee2_instance = Faculty.objects.get(email = committee2)

    limit_object = Limits.objects.get(Limit="Limit")
    if chair_instance.ischair<limit_object.ChairPerson :
        chair_instance.ischair = chair_instance.ischair+1
        chair_instance.save(update_fields=['ischair'])
    else :
        return Response({"message":"Chair Exceeded"},status=200)
    if committee1_instance.iscommem<limit_object.CommitteeLimit :
        committee1_instance.iscommem = committee1_instance.iscommem+1
        committee1_instance.save(update_fields=['iscommem'])
    else:
        return Response({"message":"committee Exceeded"},status=200)

    if committee2_instance.iscommem<limit_object.CommitteeLimit :
        committee2_instance.iscommem = committee2_instance.iscommem+1
        committee2_instance.save(update_fields=['iscommem'])
    else:
        return Response({"message":"committee Exceeded"},status=200)
    
    project_instance = Project.objects.get(rollNoId=rollno)
    if not project_instance.chair_person:
        return Response({"message":"Committee Set"},status=200)

    project_instance.chair_person = chair_instance
    project_instance.committee_members.add(committee1_instance)
    project_instance.committee_members.add(committee2_instance)
    project_instance.save(update_fields=['chair_person'])

    return Response({"message":"Success"},status=200)


@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def ViewAllEvaluations(request):
    project_instances = Project.objects.all()
    evaluation_data = ProjectSerializer(project_instances,many=True)
    return Response({"Evaluation Data":evaluation_data.data},status=200)


