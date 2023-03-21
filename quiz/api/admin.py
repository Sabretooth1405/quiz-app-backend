from django.contrib import admin
from .models import Question,FriendAnswer,Friendship,FriendshipRequests

admin.site.register(Question)
admin.site.register(FriendAnswer)
admin.site.register(Friendship)
admin.site.register(FriendshipRequests)