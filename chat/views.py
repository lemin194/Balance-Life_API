from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
import json
from rest_framework.response import Response
from .mscript import *

from rest_framework.decorators import api_view

User = get_user_model()

def index(request):
    return render(request, "chat/index.html")
def room(request, room_name):
    user = User.objects.all()[0]
    if (request.user != None):
        user = request.user
    username = user.username
    user_id = user.id
    return render(request, "chat/room.html", {
        "room_name_json": mark_safe(json.dumps(room_name)),
        "username": mark_safe(json.dumps(username)),
        "userId" : user_id,
    })



@api_view(['POST'])
def get_chatroom_name(request):
    data = request.data
    user_ids = set()
    for user_id in data['user_ids']:
        user_ids.add(user_id)
    
    room_name = generate_chat_room_name(user_ids)
    return Response({"room_name": room_name})




@api_view(['POST'])
def get_chatrooms(request):
    data = request.data
    user = User.objects.get(id=data['user_id'])
    chatrooms = ChatRoom.objects.filter(user=user)
    return Response(serialize_chatrooms(chatrooms))
