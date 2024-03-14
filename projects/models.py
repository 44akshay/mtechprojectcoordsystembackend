from django.db import models
from faculty.models import Faculty
from students.models import Student
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
# Create your models here.

# class Project(models.Model):
#     rollNoId = models.CharField(max_length=9,unique=True)
#     projectname=models.CharField(default="Default",max_length=50)
#     eval1=models.IntegerField(default=-1)
#     eval2=models.IntegerField(default=-1)
#     eval3=models.IntegerField(default=-1)
#     eval1comment=models.CharField(default="",max_length=100)
#     eval2comment=models.CharField(default="",max_length=100)
#     eval3comment=models.CharField(default="",max_length=100)
#     report1=models.URLField(max_length = 200,null=True) 
#     report2=models.URLField(max_length = 200,null=True) 
#     report3=models.URLField(max_length = 200,null=True) 
#     report1comment=models.CharField(default="",max_length=100)
#     report2comment=models.CharField(default="",max_length=100)
#     report3comment=models.CharField(default="",max_length=100)
#     report1acceptancestatus=models.BooleanField(default=False)
#     report2acceptancestatus=models.BooleanField(default=False)
#     report3acceptancestatus=models.BooleanField(default=False)
#     guide= models.ForeignKey(Faculty, on_delete=models.SET_NULL,null=True,related_name='guide_projects')
#     student = models.OneToOneField(Student,on_delete=models.SET_NULL,null=True)
#     chair_person = models.ForeignKey(Faculty,on_delete = models.CASCADE,null=True,related_name='chair_projects')
#     committee_members = models.ManyToManyField(Faculty,related_name='member_of')
StatusChoices = (
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
        ('UnderReview', 'UnderReview'),


    )
class Phase(models.Model):
    Report = models.FileField(upload_to="reports")
    Status = models.CharField(max_length=50,choices=StatusChoices,default='Pending')
    Evaluation = models.IntegerField(default=-1)
    Evaluation_Comments = models.CharField(default="", max_length=1000, blank=True)
    Report_Comments = models.CharField(default="", max_length=100, blank=True)

class Project(models.Model):
    rollNoId = models.CharField(max_length=9, unique=True)
    projectname = models.CharField(default="Default", max_length=50)
    Phase1 = models.OneToOneField(Phase,on_delete=models.SET_NULL, null=True,blank=True, related_name='project_phase1')
    Phase2 = models.OneToOneField(Phase,on_delete=models.SET_NULL, null=True,blank=True,related_name='project_phase2')
    Phase3 = models.OneToOneField(Phase,on_delete=models.SET_NULL, null=True,blank=True,related_name='project_phase3')
    guide = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True,blank=True, related_name='guide_projects')
    student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True,blank=True)
    chair_person = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True,blank=True, related_name='chair_projects')
    committee_members = models.ManyToManyField(Faculty, related_name='member_of',blank=True)

    def __str__(self):
        return f"{self.projectname}"

@receiver(post_save, sender=Student)
def my_handler(sender,created,instance, **kwargs):
    if created:
        student = Student.objects.get(email=instance.email)
        Phase1 = Phase.objects.create()
        Phase2 = Phase.objects.create()
        Phase3 = Phase.objects.create()
        proj = Project.objects.create(student=student,rollNoId=instance.rollNoId,Phase1=Phase1,Phase2=Phase2,Phase3=Phase3)
        print(proj.Phase1.Status)

@receiver(post_save, sender=Project)
def my_handler(sender,created,instance, **kwargs):
    if created:
        #student = Student.objects.get(email=instance.email)
        Phase1 = Phase.objects.create()
        Phase2 = Phase.objects.create()
        Phase3 = Phase.objects.create()
        #proj = Project.objects.create(rollNoId=instance.rollNoId,Phase1=Phase1,Phase2=Phase2,Phase3=Phase3)
        instance.Phase1 = Phase1
        instance.Phase2 = Phase2
        instance.Phase3 = Phase3
        instance.save(update_fields=['Phase1','Phase2','Phase3'])
        proj = Project.objects.get(rollNoId=instance.rollNoId)

        print(proj.Phase1.Status)

        

        