from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
# Create your models here.
class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True,default=None)
    name = models.CharField(max_length=255)
    dept=models.CharField(max_length=255)
    #counters for each role
    isguide = models.IntegerField(default=0)#guide
    ischair = models.IntegerField(default=0)#chair person
    iscommem = models.IntegerField(default=0)#committee member
    isprojcoo=models.IntegerField(default=0)#project coordinator
    email = models.CharField(max_length=30,unique=True)
    domain=models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

@receiver(post_save, sender=Faculty)
def my_handler(sender,created,instance, **kwargs):
    if created:
        user = User.objects.filter(email=instance.email)
        if not user:
            user1 = User.objects.create(username=instance.email,email=instance.email)
            user1.set_password(instance.email)
            user1.save()
            new_user = User.objects.get(email=instance.email)
            instance.user = new_user
            instance.save(update_fields=['user'])
