import json
import os
from openai import OpenAI
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.urls import reverse
from .models import Conversation, Message

# 保存聊天历史的字典，键为会话ID，值为消息列表
# 这里改为使用数据库存储，不再使用内存中的字典
# chat_histories = {}


def conversation_list(request):
    """显示对话列表"""
    conversations = Conversation.objects.all()
    context = {
        "title": "Elepathy 对话列表",
        "description": "您的所有智能对话",
        "conversations": conversations,
    }
    return render(request, "chat/html/conversation_list.html", context)


def chat_view(request, conversation_id=None):
    """
    聊天界面视图

    Args:
        conversation_id: 对话ID，如果不提供则创建新对话
    """
    # 如果没有指定对话ID，创建新对话
    if conversation_id is None:
        conversation = Conversation.objects.create(title="新对话")
        # 添加系统消息
        Message.objects.create(
            conversation=conversation,
            role="system",
            content="你是Elepathy智能助手，由大象(elephant)和共情(empathy)的组合词命名，象征着强大的记忆力和深刻的情感理解力。请提供友好、智能、有帮助的回答。请用中文回答所有问题。",
        )
        return redirect(reverse("chat:chat", args=[conversation.id]))

    # 获取指定的对话，如果不存在则404
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # 获取所有对话列表，用于侧边栏
    conversations = Conversation.objects.all()

    # 获取当前对话的消息，排除系统消息
    messages = conversation.messages.exclude(role="system").order_by("created_at")

    context = {
        "title": f"Elepathy Chat - {conversation.title}",
        "description": "通过DeepSeek强大的AI模型，与Elepathy展开智能对话，获取信息、解决问题",
        "conversation": conversation,
        "conversations": conversations,
        "messages": messages,
    }
    return render(request, "chat/html/index.html", context)


@csrf_exempt
def chat_api(request, conversation_id):
    """
    处理聊天API请求
    """
    if request.method == "POST":
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            data = json.loads(request.body)
            message_text = data.get("message", "")

            # 创建用户消息
            Message.objects.create(
                conversation=conversation, role="user", content=message_text
            )

            # 获取对话历史
            history = list(
                conversation.messages.all()
                .order_by("created_at")
                .values("role", "content")
            )

            # 调用DeepSeek API
            response_text = call_chat_api(history)

            # 创建助手回复消息
            Message.objects.create(
                conversation=conversation, role="assistant", content=response_text
            )

            # 如果是新对话且这是第一次回复，自动设置标题
            if conversation.title == "新对话" and conversation.messages.count() >= 3:
                # 尝试从第一个用户消息提取标题
                first_msg = conversation.messages.filter(role="user").first()
                if first_msg:
                    title = first_msg.content[:30] + (
                        "..." if len(first_msg.content) > 30 else ""
                    )
                    conversation.title = title
                    conversation.save()

            # 更新对话时间
            conversation.save()

            return JsonResponse(
                {
                    "status": "success",
                    "message": response_text,
                    "title": conversation.title,
                }
            )
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "仅支持POST请求"}, status=400)


def call_chat_api(messages):
    """
    使用OpenAI库调用DeepSeek API

    Args:
        messages: 聊天历史消息列表

    Returns:
        str: API返回的回复内容
    """
    try:
        # 从环境变量获取API密钥
        api_key = os.environ.get("DEEPSEEK_API_KEY") or settings.DEEPSEEK_API_KEY
        api_base = os.environ.get("DEEPSEEK_API_BASE") or settings.DEEPSEEK_API_BASE
        model = os.environ.get("DEEPSEEK_MODEL") or settings.DEEPSEEK_MODEL

        if not api_key:
            return "未配置DeepSeek API密钥，请联系管理员设置DEEPSEEK_API_KEY环境变量。"

        # 初始化OpenAI客户端，指向DeepSeek API
        client = OpenAI(
            api_key=api_key,
            base_url=api_base,  # DeepSeek的API基础URL
        )

        # 发送请求
        response = client.chat.completions.create(
            model=model,  # DeepSeek模型名称
            messages=messages,
            temperature=0.7,
            max_tokens=800,
        )

        # 获取回复内容
        return response.choices[0].message.content

    except Exception as e:
        # 记录错误
        print(f"DeepSeek API调用错误: {str(e)}")
        return f"抱歉，调用AI服务时出现了问题: {str(e)}"


@csrf_exempt
def delete_conversation(request, conversation_id):
    """删除对话"""
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, id=conversation_id)
        conversation.delete()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error", "message": "仅支持POST请求"}, status=400)


@csrf_exempt
def rename_conversation(request, conversation_id):
    """重命名对话"""
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, id=conversation_id)
        data = json.loads(request.body)
        new_title = data.get("title", "").strip()

        if new_title:
            conversation.title = new_title
            conversation.save()
            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "error", "message": "标题不能为空"}, status=400)

    return JsonResponse({"status": "error", "message": "仅支持POST请求"}, status=400)


@csrf_exempt
def clear_conversation(request, conversation_id):
    """清空对话但保留对话记录"""
    if request.method == "POST":
        conversation = get_object_or_404(Conversation, id=conversation_id)

        # 保留系统消息，删除所有其他消息
        system_msg = conversation.messages.filter(role="system").first()
        conversation.messages.exclude(id=system_msg.id if system_msg else None).delete()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "error", "message": "仅支持POST请求"}, status=400)
