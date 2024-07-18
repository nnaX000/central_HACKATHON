from django.db import models
from django.conf import settings

class User(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

class Diary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField()

class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=100)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
