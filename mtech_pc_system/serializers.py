from rest_framework import serializers
from django.contrib.auth.models import User
from projects.models import Project,Phase,Domain,Limits
from faculty.models import Faculty
from students.models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['firstname','email']

class LimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Limits
        fields = [ 'GuideLimit', 
    'ChairPerson',
    'CommitteeLimit',
    'Phase1_start',
    'Phase2_start' ,
    'Phase3_start' ,
    'Phase1_end' ,
    'Phase2_end',
    'Phase3_end']

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ['name']

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','username','email',]

class DomainSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Domain
        fields=['domain_name']
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
    committee_members = FacultySerializer(many=True)
    class Meta:
        model = Project
        fields = ['rollNoId', 'projectname', 'Phase1', 'Phase2', 'Phase3', 'guide', 'student', 'chair_person', 'committee_members']

class getRollNoSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    class Meta:
        model = Project
        fields = ['rollNoId','student']

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id','username','email',]