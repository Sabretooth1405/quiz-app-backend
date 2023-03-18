from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import localtime

class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=140)
    description=models.TextField(blank=True)
    date = models.DateField(default=datetime.date.today)
    created_at = models.DateTimeField(default=localtime)
