from django.shortcuts import render
from team.models import TeamMember


def view(request):
    """
    团队页面视图
    """
    context = {
        "title": "Elepathy 团队 - 共同构建智慧共情的未来",
        "description": "了解 Elepathy 背后的创新团队，我们致力于创造智能、人性化的工具和服务。",
        "team_members": [],  # 先使用空列表
    }
    from django.db import connection

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='team_teammember';"
        )

    # 从数据库获取团队成员信息
    team_members = TeamMember.objects.all()

    # 如果没有成员数据，创建一些示例数据
    if not team_members.exists():
        create_sample_team_members()
        team_members = TeamMember.objects.all()

    context["team_members"] = team_members

    return render(request, "team/index.html", context)


def create_sample_team_members():
    """创建示例团队成员数据（仅用于开发）"""
    # 检查是否已有数据
    if TeamMember.objects.count() > 0:
        return  # 如果已有数据则不创建

    # 创建示例数据
    TeamMember.objects.create(
        name="王weidong",
        role="创始人 & 首席开发者",
        email="1598593280@qq.com",
        github_url="https://github.com/WangWindow",
        avatar_path="/static/images/team/avatar-1.png",
        order=1,
    )

    TeamMember.objects.create(
        name="袁xueyu",
        role="前端开发",
        avatar_path="/static/images/team/avatar-2.webp",
        order=2,
    )

    TeamMember.objects.create(
        name="董jiaxuan",
        role="后端开发",
        avatar_path="/static/images/team/avatar-3.webp",
        order=3,
    )

    TeamMember.objects.create(
        name="陈xi",
        role="UI/UX 设计",
        avatar_path="/static/images/team/avatar-4.webp",
        order=4,
    )

    TeamMember.objects.create(
        name="周zuowei",
        role="系统运维",
        avatar_path="/static/images/team/avatar-5.webp",
        order=5,
    )
