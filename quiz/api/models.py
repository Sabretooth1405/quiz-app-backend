from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import localtime


class Question(models.Model):
    class Month(models.TextChoices):
        GEN = "GEN", "GENERAL"
        MUS = "MUS", "MUSIC"
        ENT = "ENT", "ENTERTAINMENT"
        LIT = "LIT", "LITERATURE"
        ART = "ART", "ART"
        SPO = "SPO", "SPORT"
        SCI = "SCI", "SCIENCE"
        BIZ = "BIZ", "BUSINESS"
        TEC = "TEC", "TECHNOLOGY"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=3, choices=Month.choices, default=Month.GEN)
    question = models.TextField(blank=True)
    question_urls = models.JSONField(blank=True,null=True)
    answer = models.TextField(blank=True)
    answer_urls = models.JSONField(blank=True,null=True)
    created_at = models.DateTimeField(default=localtime)
    used=models.BooleanField(default=False)