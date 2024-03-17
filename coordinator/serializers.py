from rest_framework import serializers
from django.contrib.auth.models import User
from projects.models import Project,Phase,Domain,Limits
from faculty.models import Faculty
from students.models import Student






class PhaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Phase
        fields = [  'Evaluation']

class ProjectSerializer(serializers.ModelSerializer):
    Phase1 = PhaseSerializer()
    Phase2 = PhaseSerializer()
    Phase3 = PhaseSerializer()
    # guide = FacultySerializer()
    # chair_person = FacultySerializer()
    # committee_members = FacultySerializer(many=True)
    class Meta:
        model = Project
        fields = ['rollNoId', 'projectname', 'Phase1', 'Phase2', 'Phase3']

