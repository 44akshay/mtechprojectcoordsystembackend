from django.db import models
from django.contrib.auth.models import User
#from projects.models import Project
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
#from myapp.models import My




        #User.save()
# Create your models here.

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,default=None)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    rollNoId = models.CharField(max_length=9,unique=True)
    email = models.CharField(max_length=30,unique=True)
    semester = models.IntegerField()
    program = models.CharField(default="M.tech",max_length=50)
    # = model.boolField()
    isGuideSelected=models.BooleanField(default=False)
    
 #  Guide = models.ForeignKey(Faculty,onS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_name = models.CharField(max_length=255, null=True, blank=True)
    

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


@receiver(post_save, sender=Student)
def my_handler(sender,created,instance, **kwargs):
    if created:
        user = User.objects.filter(email=instance.email)
        if not user:
            user1 = User.objects.create(username=instance.email,email=instance.email)
            #Project.objects.create(student=user)
            user1.set_password(instance.rollNoId)
            user1.save()
            new_user = User.objects.get(email=instance.email)

            instance.user = new_user
            instance.save(update_fields=['user'])


# class Reports(models.Model):
#     Student =  
