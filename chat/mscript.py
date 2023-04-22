
import hashlib
from .models import ChatRoom, Message
from food.serializers import UserSerializer


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

def serialize_user(user):
    return UserSerializer(user, many=False).data

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
        "user_ids": []
    }
    for user_value in chatroom.user.values_list():
        ret['user_ids'].append(user_value[0])
    
    return ret

def serialize_chatrooms(chatrooms):
    ret = []
    for chatroom in chatrooms:
        ret.append(serialize_chatroom(chatroom))
    return ret
