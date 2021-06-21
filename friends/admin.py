from django.contrib import admin
from .models import Friend, FriendRequest,Invoice


admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(Invoice)
