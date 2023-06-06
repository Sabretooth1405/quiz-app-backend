from django.contrib import admin
from .models import Question,FriendAnswer,Friendship,FriendshipRequests,FriendshipAdmin,FriendshipRequestAdmin

admin.site.register(Question)
admin.site.register(FriendAnswer)
admin.site.register(Friendship,FriendshipAdmin)
admin.site.register(FriendshipRequests,FriendshipRequestAdmin)