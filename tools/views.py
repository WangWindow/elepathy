"""
==============================================================================
 * @FilePath: views.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-25 23:20:29
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-25 23:25:32
 * @Copyright © 2025 WangWindow
 * @Descripttion:
==============================================================================
"""

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the tools index.")
