"""
==============================================================================
 * @FilePath: urls.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-25 23:29:57
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-25 23:30:15
 * @Copyright © 2025 WangWindow
 * @Descripttion:
==============================================================================
"""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
