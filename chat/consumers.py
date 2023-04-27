# chat/consumers.py
from django.contrib.auth import get_user_model

import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.db import database_sync_to_async


from django.db.models.fields.files import ImageFieldFile
from .mscript import *
import base64
import os
import re
from django.utils import timezone

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):

    def get_recent_messages(self):
        return list(Message.objects.filter(chatroom_name=self.room_name).order_by("timestamp"))[-20:]
    async def fetch_messages(self, data):
        messages = await database_sync_to_async(self.get_recent_messages)()
        content = {
            'command' : "messages",
            'messages': await database_sync_to_async(messages_to_json)(messages)
        }
        await self.send_message(content)
    
    def sync_new_message(self, data): 
        
        message_json = data['message']
        author_id = message_json['author']
        author_user = User.objects.filter(id=author_id)[0]
        message = Message.objects.create(
            author=author_user, 
            content=message_json['content'],
            chatroom_name=self.room_name,
        )
        print('create_message', message)

        user_ids = {message_json['author'], data['target']}
        chatroom = ChatRoom.objects.get_or_create(name=self.room_name)[0]
        for user_id in user_ids:
            chatroom.user.add(User.objects.get(id=user_id))
        chatroom.last_message_sent = message
        chatroom.save()
        
        send_data = {
            'command': 'new_message',
            'message': message_to_json(message),
        }
        return send_data

    async def new_message(self, data):
        send_data = await database_sync_to_async(self.sync_new_message)(data)
        return await self.send_chat_message(send_data)
    

    def sync_new_image_message(self, data):
        filename_with_extension = data['file']['filename']
        (filename, extension) = os.path.splitext(filename_with_extension)
        
        image_content = data['file']['content']
        decoded_content = base64.b64decode(image_content)
        newfilename = "images/chatroom/" + self.room_name + "/" \
            + filename + re.sub(r'[+:. ]', '-', str(timezone.now())) + extension
        
        os.makedirs(os.path.dirname("media/" + newfilename), exist_ok=True)
        with open("media/" + newfilename, 'wb') as f:
            f.write(decoded_content)

        
        message_json = data['message']
        author_id = message_json['author']
        author_user = User.objects.filter(id=author_id)[0]
        message = Message.objects.create(
            author=author_user, 
            chatroom_name=self.room_name,
        )
        message.image_content.name = newfilename
        message.message_type = "Image"
        message.save()

        user_ids = {message_json['author'], data['target']}
        chatroom = ChatRoom.objects.get_or_create(name=self.room_name)[0]
        for user_id in user_ids:
            chatroom.user.add(User.objects.get(id=user_id))
        chatroom.last_message_sent = message
        chatroom.save()
        send_data = {
            'command': 'new_message',
            'message': message_to_json(message),
        }
        return send_data

    async def new_image_message(self, data):
        send_data = await database_sync_to_async(self.sync_new_image_message)(data)
        return await self.send_chat_message(send_data)


    def sync_new_group_message(self, data):
        message_json = data['message']
        author_user_id = message_json['author']
        author_user = User.objects.get(id=author_user_id)
        message = Message.objects.create(
            author = author_user,
            content = message_json['content'],
            chatroom_name=self.room_name,
        )

        chatroom = ChatRoom.objects.get_or_create(name=self.room_name)[0]
        chatroom.last_message_sent = message
        chatroom.user.add(author_user)
        chatroom.save()

        send_data = {
            'command' : "new_message",
            "message" : message_to_json(message)
        }
        return send_data

    async def new_group_message(self, data):
        send_data = await database_sync_to_async(self.sync_new_group_message)(data)
        return await self.send_chat_message(send_data)

        
    async def create_chat_room(self, data):
        user_ids = set()
        for user_id in data['user_ids']:
            user_ids.add(user_id)
        
        chatroom = ChatRoom.objects.get_or_create(name=generate_chat_room_name(user_ids))[0]
        for user_id in user_ids :
            user = User.objects.get(id = user_id)
            chatroom.user.add(user)
        
        chatroom.save()
    
    def sync_read_messages(self, data):
        user_id = data['user_id']

        send_data = {"status": "OK"}
        self.chatroom = self.get_chatroom()
        print(self.chatroom)
        if (not self.chatroom):
            return {"status": "ERROR"}
        
        lastmessagereadinstance = self.chatroom.lastmessagereadinstance_set.get_or_create(
            chatroom=self.chatroom,
            user=User.objects.get(id=user_id)
        )[0]
        lastmessagereadinstance.message = self.chatroom.last_message_sent
        lastmessagereadinstance.save()
        

        return send_data
    async def read_messages(self, data): 
        send_data = await database_sync_to_async(self.sync_read_messages)(data)

        if (send_data['status'] == "OK"):
            await self.reload_chatroom()
            await self.update_chatrooms()
            return
        return

    def sync_reload_chatroom(self):
        
        self.chatroom = self.get_chatroom()
        send_data = {
            "command": "reload_chatroom",
            "chatroom": serialize_chatroom(self.chatroom),
        }
        return send_data

    async def reload_chatroom(self):
        send_data = await database_sync_to_async(self.sync_reload_chatroom)()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_newupdate",
                "message": send_data
            }
        )


    commands = {
        'fetch_messages': fetch_messages,
        'new_message' : new_message,
        'create_chat_room': create_chat_room,
        'new_group_message': new_group_message,
        'new_image_message': new_image_message,
        'read_messages' : read_messages,
        'reload_chatroom': reload_chatroom,
    }

    
    def get_chatroom(self):
        chatrooms = ChatRoom.objects.filter(name=self.room_name)
        if (len(chatrooms) == 0):
            return None
        chatroom = chatrooms[0]
        return chatroom
    def get_all_user(self):
        if (not self.chatroom):
            self.chatroom = get_chatroom()
            if (not self.chatroom):
                return
        user_list = []
        for user in self.chatroom.user.all():
            user_list.append(user)
        
        return user_list
    

    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        
        
        self.chatroom = await database_sync_to_async(self.get_chatroom)()
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name
        )


        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        await self.commands[data['command']](self, data)


    async def update_chatrooms(self):
        
        user_list = await database_sync_to_async(self.get_all_user)()
        
        for user in user_list:
            await self.channel_layer.group_send(
                "chatrooms_%s" % user.id,
                {
                    "type": "chatrooms.newupdate",
                    "message" : {
                        "command": "get_all_chatrooms",
                    }
                }
            )

    async def send_chat_message(self, message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message
            }
        )
        if not self.chatroom:
            self.chatroom = await database_sync_to_async(self.get_chatroom)()
        
        await self.update_chatrooms()


    async def send_message(self, message):
        await self.send(text_data=json.dumps(message))
    

    async def chat_newupdate(self, event):
        send_data = event['message']
        await self.send(text_data=json.dumps(send_data))

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps(message))






class ChatRoomsConsumer(WebsocketConsumer):

    def get_all_chatrooms(self, data):
        chatrooms = ChatRoom.objects.filter(user=self.user)
        send_data = {
            "command": "get_all_chatrooms",
            "chatrooms": serialize_chatrooms(chatrooms),
        }
        return self.send_message(send_data)

    def reload_chatroom_by_id(self, data):
        chatroom = ChatRoom.objects.get(id = data['id'])
        send_data = {
            "command": "reload_chatroom_by_id",
            "chatroom": serialize_chatroom(chatroom),
        }
        return self.send_message(send_data)
    def get_all_friends(self, data):
        friendList = []
        for user in User.objects.all():
            if (user.id != self.user_id):
                friendList.append(user)
        send_data = {
            "command": "get_all_friends",
            "friend_list": serialize_users(friendList),
        }

    commands = {
        "get_all_chatrooms": get_all_chatrooms,
        "get_all_friends": get_all_friends,
        "reload_chatroom_by_id": reload_chatroom_by_id,
    }

    def connect(self):
        self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        print(self.user_id)
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_group_name = "chatrooms_%s" % self.room_name
        print(self.room_group_name)

        self.user = User.objects.get(id=self.user_id)
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )


        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )


    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)


    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chatrooms_newupdate(self, event):
        message = event['message']
        self.commands[message['command']](self, message)