
import hashlib
from .models import ChatRoom, Message
from food.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


def generate_chat_room_name(user_ids):
    str2hash = ""
    for user_id in user_ids:
        str2hash += str(user_id) + "-"
    roomhash = hashlib.md5(str2hash.encode())
    return roomhash.hexdigest()


def messages_to_json(messages):
    result = []
    for message in messages:
        result.append(message_to_json(message))
    return result

def message_to_json(message : Message):
    user_json = UserSerializer(message.author, many=False).data
    result = {
        "id": message.id,
        "author": user_json,
        "message_type": message.message_type,
        "timestamp": str(message.timestamp),
    }
    if (message.message_type == "Text"):
        result.update({
            'content': message.content,
        })
    elif message.message_type == "Image":
        result.update({
            'content': message.image_content.url
        })
    return result

def serialize_user(user : User):
    ret = {
        'id': user.id,
        'profile_image': '',
        'last_login': user.last_login,
        'username' : user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'date_joined': user.date_joined,
        'role': user.role,
    }
    return ret

def serialize_users(users):
    ret = []
    for user in users:
        ret.append(serialize_user(user))
    return ret

def serialize_chatroom(chatroom:ChatRoom):
    ret = {
        "id": chatroom.id,
        "name": chatroom.name,
        "last_message_sent": message_to_json(chatroom.last_message_sent),
        "user_ids": [],
        "last_message_read": {},
    }
    for user_value in chatroom.user.values_list():
        user_id = user_value[0]
        ret['user_ids'].append(user_id)
    for last_message_read_value in chatroom.lastmessagereadinstance_set.values_list():
        user_id = last_message_read_value[1]
        message_id = last_message_read_value[2]
        chatroom_id = last_message_read_value[3]
        ret['last_message_read'].update({user_id: message_id})
    
    return ret

def serialize_chatrooms(chatrooms):
    ret = []
    for chatroom in chatrooms:
        ret.append(serialize_chatroom(chatroom))
    return ret
