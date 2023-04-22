from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("chatroom/<str:room_name>/", views.room, name="room"),
    path("get_chatroom_name/", views.get_chatroom_name, name="get_chatroom_name"),
    path("get_chatrooms/", views.get_chatrooms, name="get_chatrooms")
]