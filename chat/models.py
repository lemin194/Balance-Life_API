from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Message(models.Model):
    class MessageType(models.TextChoices):
        TEXT = "Text"
        IMAGE = "Image"
        VIDEO = "Video"
    message_type = models.CharField(max_length=50, choices=MessageType.choices, default="Text")
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image_content = models.ImageField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    chatroom_name = models.CharField(max_length=50)
    is_liked = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.author} - {self.timestamp}'

    def last_10_messages():
        return Message.objects.order_by('timestamp').all()[:10]


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    user = models.ManyToManyField(User)
    last_message_sent = models.ForeignKey(Message, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):

        return f'{self.name}'


class LastMessageReadInstance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user.id} - {self.message.id}'