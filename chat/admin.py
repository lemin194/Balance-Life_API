from django.contrib import admin
from .models import Message, ChatRoom

admin.site.register(ChatRoom)
admin.site.register(Message)