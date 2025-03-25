"""
==============================================================================
 * @FilePath: views.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-25 23:28:50
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-25 23:33:32
 * @Copyright © 2025 WangWindow
 * @Descripttion:
==============================================================================
"""

from django.shortcuts import render


def index(request):
    context = {
        "title": "Elepathy - 智慧共情的力量",
        "description": "如同大象般强大的记忆力与情感共鸣的完美结合",
    }
    return render(request, "home/index.html", context)
