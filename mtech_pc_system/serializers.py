from rest_framework import serializers
from django.contrib.auth.models import User
from projects.models import Project,Phase
from faculty.models import Faculty

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','username','email',]

class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = ['Report', 'Status', 'Evaluation', 'Evaluation_Comments', 'Report_Comments']

class ProjectSerializer(serializers.ModelSerializer):
    Phase1 = PhaseSerializer()
    Phase2 = PhaseSerializer()
    Phase3 = PhaseSerializer()
    guide = FacultySerializer()
    chair_person = FacultySerializer()
    committee_members = FacultySerializer()
    class Meta:
        model = Project
        fields = ['rollNoId', 'projectname', 'Phase1', 'Phase2', 'Phase3', 'guide', 'student', 'chair_person', 'committee_members']

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','username','email',]