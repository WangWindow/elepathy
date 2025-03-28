from django.test import TestCase, Client
from django.urls import reverse
import json
from unittest.mock import patch
from .models import Conversation, Message


class ConversationModelTest(TestCase):
    """测试对话模型"""

    def test_create_conversation(self):
        """测试创建对话"""
        conversation = Conversation.objects.create(title="测试对话")
        self.assertEqual(str(conversation), "测试对话")
        self.assertIsNotNone(conversation.id)
        self.assertEqual(conversation.title, "测试对话")


class MessageModelTest(TestCase):
    """测试消息模型"""

    def setUp(self):
        self.conversation = Conversation.objects.create(title="测试对话")

    def test_create_message(self):
        """测试创建消息"""
        message = Message.objects.create(
            conversation=self.conversation, role="user", content="你好，AI助手"
        )
        self.assertEqual(str(message), "user: 你好，AI助手")
        self.assertIsNotNone(message.id)
        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "你好，AI助手")
        self.assertEqual(message.conversation, self.conversation)

    def test_message_ordering(self):
        """测试消息排序"""
        message1 = Message.objects.create(
            conversation=self.conversation, role="user", content="第一条消息"
        )
        message2 = Message.objects.create(
            conversation=self.conversation, role="assistant", content="第二条消息"
        )
        # 按创建时间升序排列
        messages = Message.objects.all()
        self.assertEqual(messages[0], message1)
        self.assertEqual(messages[1], message2)


class ChatViewTest(TestCase):
    """测试聊天视图"""

    def setUp(self):
        self.client = Client()
        self.conversation = Conversation.objects.create(title="测试对话")
        # 添加系统消息
        self.system_message = Message.objects.create(
            conversation=self.conversation,
            role="system",
            content="你是Elepathy智能助手",
        )
        # 添加用户消息
        self.user_message = Message.objects.create(
            conversation=self.conversation, role="user", content="你好"
        )
        # 添加助手消息
        self.assistant_message = Message.objects.create(
            conversation=self.conversation,
            role="assistant",
            content="你好！有什么可以帮你的吗？",
        )

    def test_conversation_list_view(self):
        """测试对话列表视图"""
        url = reverse("chat:conversation_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/html/conversation_list.html")
        self.assertContains(response, "测试对话")

    def test_new_chat_view(self):
        """测试新建对话视图"""
        url = reverse("chat:new_chat")
        response = self.client.get(url)
        # 应该重定向到新创建的对话
        self.assertEqual(response.status_code, 302)
        # 检查是否创建了新对话
        self.assertEqual(Conversation.objects.count(), 2)
        # 检查新对话的消息数量
        new_conversation = Conversation.objects.latest("created_at")
        # 修改这一行，根据实际实现来验证消息数量
        self.assertEqual(new_conversation.messages.count(), 1)
        # 检查第一条消息是否为系统消息
        self.assertEqual(new_conversation.messages.first().role, "system")

    def test_chat_view(self):
        """测试聊天视图"""
        url = reverse("chat:chat", args=[self.conversation.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "chat/html/index.html")
        self.assertContains(response, "测试对话")
        # 检查是否包含消息内容，但不包含系统消息
        self.assertContains(response, "你好")
        self.assertContains(response, "你好！有什么可以帮你的吗？")
        self.assertNotContains(response, "你是Elepathy智能助手")


class ChatApiTest(TestCase):
    """测试聊天API"""

    def setUp(self):
        self.client = Client()
        self.conversation = Conversation.objects.create(title="测试对话")
        # 添加系统消息
        self.system_message = Message.objects.create(
            conversation=self.conversation,
            role="system",
            content="你是Elepathy智能助手",
        )

    @patch("chat.views.call_chat_api")
    def test_chat_api(self, mock_call_chat_api):
        """测试聊天API"""
        # 模拟AI响应
        mock_call_chat_api.return_value = "我是Elepathy智能助手，很高兴为您服务！"

        url = reverse("chat:chat_api", args=[self.conversation.id])
        data = {"message": "请介绍一下你自己"}
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

        # 检查响应状态
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertEqual(response_data["status"], "success")
        self.assertEqual(
            response_data["message"], "我是Elepathy智能助手，很高兴为您服务！"
        )

        # 检查是否创建了新消息
        self.assertEqual(
            self.conversation.messages.count(), 3
        )  # 系统消息 + 用户消息 + 助手消息
        user_message = self.conversation.messages.filter(role="user").first()
        self.assertEqual(user_message.content, "请介绍一下你自己")
        assistant_message = self.conversation.messages.filter(role="assistant").first()
        self.assertEqual(
            assistant_message.content, "我是Elepathy智能助手，很高兴为您服务！"
        )

        # 检查mock函数是否被调用
        mock_call_chat_api.assert_called_once()


class ConversationActionsTest(TestCase):
    """测试对话操作"""

    def setUp(self):
        self.client = Client()
        self.conversation = Conversation.objects.create(title="测试对话")
        # 添加系统消息
        self.system_message = Message.objects.create(
            conversation=self.conversation,
            role="system",
            content="你是Elepathy智能助手",
        )
        # 添加用户消息
        self.user_message = Message.objects.create(
            conversation=self.conversation, role="user", content="你好"
        )
        # 添加助手消息
        self.assistant_message = Message.objects.create(
            conversation=self.conversation,
            role="assistant",
            content="你好！有什么可以帮你的吗？",
        )

    def test_rename_conversation(self):
        """测试重命名对话"""
        url = reverse("chat:rename_conversation", args=[self.conversation.id])
        data = {"title": "重命名后的对话"}
        response = self.client.post(
            url, json.dumps(data), content_type="application/json"
        )

        # 检查响应状态
        self.assertEqual(response.status_code, 200)
        # 检查是否更新了标题
        self.conversation.refresh_from_db()
        self.assertEqual(self.conversation.title, "重命名后的对话")

    def test_clear_conversation(self):
        """测试清空对话"""
        url = reverse("chat:clear_conversation", args=[self.conversation.id])
        response = self.client.post(url)

        # 检查响应状态
        self.assertEqual(response.status_code, 200)
        # 检查是否清空了消息，但保留了系统消息
        self.conversation.refresh_from_db()
        self.assertEqual(self.conversation.messages.count(), 1)
        self.assertEqual(self.conversation.messages.first().role, "system")

    def test_delete_conversation(self):
        """测试删除对话"""
        url = reverse("chat:delete_conversation", args=[self.conversation.id])
        response = self.client.post(url)

        # 检查响应状态
        self.assertEqual(response.status_code, 200)
        # 检查是否删除了对话
        self.assertEqual(Conversation.objects.count(), 0)
        # 检查是否级联删除了消息
        self.assertEqual(Message.objects.count(), 0)
