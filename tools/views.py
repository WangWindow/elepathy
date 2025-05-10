from django.shortcuts import render
from .models import Tool


def index(request):
    tools = Tool.objects.all().order_by("-created_at")
    for tool in tools:
        tool.tags_list = tool.tag_list()
    context = {
        "title": "实用工具箱 - Elepathy",
        "description": "发现和使用丰富的在线工具，助力高效工作与生活。",
        "tools": tools,
    }
    return render(request, "tools/index.html", context)
