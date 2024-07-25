from django.db import models
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

from datetime import date, time

class EveryList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    due_date = models.DateField(default=date.today)
    due_time = models.TimeField(default=time.min)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task

class LifeList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    target_date = models.DateField(default=date.today)
    target_time = models.TimeField(default=time.min)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.goal
