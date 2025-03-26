"""
==============================================================================
 * @FilePath: views.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-26 11:09:32
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-26 11:12:02
 * @Copyright © 2025 WangWindow
 * @Descripttion:
==============================================================================
"""

from django.shortcuts import render


def view(request):
    """
    团队页面视图
    """
    context = {
        "title": "Elepathy 团队 - 共同构建智慧共情的未来",
        "description": "了解 Elepathy 背后的创新团队，我们致力于创造智能、人性化的工具和服务。",
    }
    return render(request, "team/html/index.html", context)
