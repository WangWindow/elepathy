from django.urls import path
from . import views

app_name = "chat"

urlpatterns = [
    # 对话列表
    path("", views.conversation_list, name="conversation_list"),
    # 新建对话
    path("new/", views.chat_view, name="new_chat"),
    # 具体对话
    path("<uuid:conversation_id>/", views.chat_view, name="chat"),
    # 对话API
    path("<uuid:conversation_id>/api/", views.chat_api, name="chat_api"),
    # 删除对话
    path(
        "<uuid:conversation_id>/delete/",
        views.delete_conversation,
        name="delete_conversation",
    ),
    # 重命名对话
    path(
        "<uuid:conversation_id>/rename/",
        views.rename_conversation,
        name="rename_conversation",
    ),
    # 清空对话内容
    path(
        "<uuid:conversation_id>/clear/",
        views.clear_conversation,
        name="clear_conversation",
    ),
]
