from django.contrib import admin
from .models import Message, ChatRoom, LastMessageReadInstance

admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(LastMessageReadInstance)