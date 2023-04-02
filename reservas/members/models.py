from django.db import models
from django.contrib.auth.models import User, BaseUserManager

# Create your models here.

class Members(models.Model):
    Member=models.OneToOneField(User,on_delete=models.SET_NULL, max_length=50,null=True,verbose_name='User', related_name='User' )
    def __str__(self):
        return self.Member.username
    
    class Meta:
        verbose_name_plural = 'Members'