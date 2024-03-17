from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from projects.models import *

class chairpSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Project
        fields = ['rollNoId','projectname']
class PhaseSerializer1(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['Report', 'Status', 'Evaluation', 'Evaluation_Comments', 'Report_Comments']
class FacultySerializer1(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']
class ProjectSerializer1(serializers.ModelSerializer):
    Phase1 = PhaseSerializer1()
    Phase2 = PhaseSerializer1()
    Phase3 = PhaseSerializer1()
    guide = FacultySerializer1()
    chair_person = FacultySerializer1()
    committee_members = FacultySerializer1(many=True)
    class Meta:
        model = Project
        fields = ['rollNoId', 'projectname', 'Phase1', 'Phase2', 'Phase3', 'guide', 'student', 'chair_person', 'committee_members']
