from django.db import models
from django.contrib.auth.models import User  
import datetime

class Client(models.Model):
    client_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
                                                                                           
    def __str__(self):
        return self.client_name


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    client = models.ForeignKey(Client, related_name='projects', on_delete=models.CASCADE)
    users = models.ManyToManyField(User, related_name='projects')
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='projects_created', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.project_name


class ProjectAssignment(models.Model):
    project = models.ForeignKey(Project, related_name="assignments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="assigned_projects", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('project', 'user')



