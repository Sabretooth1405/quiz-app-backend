from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import localtime
from django.contrib import admin

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
        HIS = "HIS", "HISTORY"
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=3, choices=Month.choices, default=Month.GEN)
    question = models.TextField(blank=True)
    question_urls = models.JSONField(blank=True, null=True)
    answer = models.TextField(blank=True)
    answer_urls = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(default=localtime)
    used = models.BooleanField(default=False)
    used_for = models.TextField(default="UNASSIGNED")
    visible_to_friends = models.BooleanField(default=False)
    make_answer_visible= models.BooleanField(default=False)
    def __str__(self):
        return self.question[:20]


class FriendAnswer(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    answerer=models.ForeignKey(User,on_delete=models.CASCADE)
    answer_given=models.TextField(default="")
    is_checked=models.BooleanField(default=False)
    is_correct=models.BooleanField(default=False)
    answered_at=models.DateTimeField(default=localtime)
    is_cleaned=False
    def clean(self):
        self.is_cleaned = True
        if self.answerer == self.question.user:
            print(self.answerer,self.question)
            raise ValidationError("You cannot answer your own question")
        super(FriendAnswer, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(FriendAnswer, self).save(*args, **kwargs)


    class Meta:
        unique_together = ("question", "answerer")
    def __str__(self):
        return f'{self.question.question[:10]} {self.answerer.username}'

class Friendship(models.Model):
    # you
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fs_from",
       
    )
    # your friend
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fs_to",
       
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("from_user", "to_user")
class FriendshipAdmin(admin.ModelAdmin):
    list_display=('from_user','to_user','created_at',)

class FriendshipRequests(models.Model):
    is_cleaned = False
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fr_from",
        
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="fr_to",
        
    )

    created = models.DateTimeField(auto_now_add=True, editable=False)
    rejected = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def clean(self):
        self.is_cleaned = True
        if self.rejected is True and self.accepted is True:
            raise ValidationError(
                "Both rejected and accepted cannot be True at the same time."
            )
        if self.to_user == self.from_user:
            raise ValidationError("You cannot friend yourself")
        super(FriendshipRequests, self).clean()

    def save(self, *args, **kwargs):
        if not self.is_cleaned:
            self.full_clean()
        super(FriendshipRequests, self).save(*args, **kwargs)

    class Meta:
        unique_together = ("from_user", "to_user")
class FriendshipRequestAdmin(admin.ModelAdmin):
    list_display=('from_user','to_user','created','rejected','accepted','is_cleaned')