from django.test import TestCase, Client
from django.urls import reverse
from .models import TeamMember


class TeamViewTest(TestCase):
    """团队页面视图测试"""

    def setUp(self):
        """测试前准备"""
        self.client = Client()
        # 创建测试团队成员
        TeamMember.objects.create(
            name="测试成员",
            role="测试角色",
            bio="这是一个测试成员的简介",
            email="test@example.com",
            avatar_path="/static/images/team/avatar-1.png",
            github_url="https://github.com/testuser",
            order=1,
        )

    def test_team_view_status_code(self):
        """测试团队页面视图状态码"""
        url = reverse("team:team")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_team_view_template(self):
        """测试团队页面使用的模板"""
        url = reverse("team:team")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "team/html/index.html")

    def test_team_view_context(self):
        """测试团队页面视图传递的上下文数据"""
        url = reverse("team:team")
        response = self.client.get(url)
        self.assertIn("title", response.context)
        self.assertIn("description", response.context)
        self.assertEqual(
            response.context["title"], "Elepathy 团队 - 共同构建智慧共情的未来"
        )
        self.assertEqual(
            response.context["description"],
            "了解 Elepathy 背后的创新团队，我们致力于创造智能、人性化的工具和服务。",
        )
        self.assertIn("team_members", response.context)
        self.assertTrue(len(response.context["team_members"]) >= 1)

    def test_team_view_content(self):
        """测试团队页面内容"""
        url = reverse("team:team")
        response = self.client.get(url)
        self.assertContains(response, "我们的团队")
        self.assertContains(response, "关于我们")
        self.assertContains(response, "我们的价值观")
        self.assertContains(response, "团队成员")
        self.assertContains(response, "加入我们")
        # 检查是否包含团队成员信息
        self.assertContains(response, "测试成员")
        self.assertContains(response, "测试角色")
        self.assertContains(response, "这是一个测试成员的简介")

    def test_sample_data_creation(self):
        """测试自动创建样本数据功能"""
        # 先删除所有现有数据
        TeamMember.objects.all().delete()
        # 访问页面应该触发示例数据创建
        url = reverse("team:team")
        self.client.get(url)
        # 验证有数据被创建
        self.assertTrue(TeamMember.objects.exists())
        # 验证创建了5个示例成员
        self.assertEqual(TeamMember.objects.count(), 5)
        # 验证包含特定成员
        self.assertTrue(TeamMember.objects.filter(name="王weidong").exists())


class TeamMemberModelTest(TestCase):
    """团队成员模型测试"""

    def test_create_team_member(self):
        """测试创建团队成员"""
        member = TeamMember.objects.create(
            name="测试成员",
            role="测试角色",
            bio="这是一个测试成员的简介",
            email="test@example.com",
            avatar_path="/static/images/team/avatar-1.png",
            github_url="https://github.com/testuser",
            order=1,
        )
        self.assertEqual(str(member), "测试成员 - 测试角色")
        self.assertEqual(member.name, "测试成员")
        self.assertEqual(member.role, "测试角色")
        self.assertEqual(member.email, "test@example.com")
        self.assertEqual(member.avatar_path, "/static/images/team/avatar-1.png")
        self.assertEqual(member.order, 1)

    def test_team_member_ordering(self):
        """测试团队成员排序"""
        member1 = TeamMember.objects.create(name="成员1", role="角色1", order=2)
        member2 = TeamMember.objects.create(name="成员2", role="角色2", order=1)
        # 按 order 字段升序排列
        members = TeamMember.objects.all()
        self.assertEqual(members[0], member2)  # order=1 应该排在前面
        self.assertEqual(members[1], member1)  # order=2 应该排在后面


class TeamIntegrationTest(TestCase):
    """团队功能集成测试"""

    def setUp(self):
        self.client = Client()

    def test_team_page_displays_all_members(self):
        """测试团队页面显示所有成员"""
        # 创建3个测试成员
        for i in range(1, 4):
            TeamMember.objects.create(
                name=f"测试成员{i}",
                role=f"测试角色{i}",
                avatar_path=f"/static/images/team/avatar-{i}.png",
                order=i,
            )

        url = reverse("team:team")
        response = self.client.get(url)

        # 验证所有成员都显示在页面上
        for i in range(1, 4):
            self.assertContains(response, f"测试成员{i}")
            self.assertContains(response, f"测试角色{i}")
            self.assertContains(response, f'src="/static/images/team/avatar-{i}.png"')

    def test_member_without_avatar_path(self):
        """测试没有头像路径的成员在页面上的显示"""
        # 创建一个没有头像路径的成员
        TeamMember.objects.create(
            name="无头像成员",
            role="测试角色",
            order=5,
        )

        url = reverse("team:team")
        response = self.client.get(url)

        # 验证成员信息正确显示
        self.assertContains(response, "无头像成员")
        self.assertContains(response, "测试角色")
        # 验证页面仍然能正常加载无头像成员
        self.assertEqual(response.status_code, 200)
