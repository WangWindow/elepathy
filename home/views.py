from django.shortcuts import render


def home(request):
    """
    首页视图
    """
    context = {
        "title": "Elepathy - 智慧共情的力量",
        "description": "通过强大的记忆力和深刻的情感理解力，提供智能、人性化、可靠的工具和服务。",
    }
    return render(request, "home/index.html", context)
