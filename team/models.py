"""
==============================================================================
 * @FilePath: models.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-26 11:09:32
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-28 13:31:17
 * @Copyright © 2025 WangWindow
 * @Descripttion:
==============================================================================
"""

from django.db import models


class TeamMember(models.Model):
    """团队成员模型"""

    name = models.CharField("姓名", max_length=100)
    role = models.CharField("角色", max_length=100)
    bio = models.TextField("简介", blank=True)
    email = models.EmailField("邮箱", blank=True)
    avatar_path = models.CharField("头像路径", max_length=255, blank=True)
    github_url = models.URLField("GitHub 链接", blank=True)
    order = models.PositiveIntegerField("排序", default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "团队成员"
        verbose_name_plural = "团队成员"

    def __str__(self):
        return f"{self.name} - {self.role}"
