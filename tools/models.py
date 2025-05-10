from django.db import models


class Tool(models.Model):
    """工具模型"""

    name = models.CharField("工具名称", max_length=100)
    description = models.TextField("工具描述", blank=True)
    icon = models.CharField(
        "图标类名", max_length=100, blank=True, default="fas fa-tools"
    )
    tags = models.CharField("标签（逗号分隔）", max_length=200, blank=True)
    status = models.CharField(
        "状态",
        max_length=20,
        choices=[("beta", "Beta"), ("stable", "Stable")],
        default="stable",
    )
    url = models.URLField("工具链接", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]

    def __str__(self):
        return self.name
