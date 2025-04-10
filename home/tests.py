from django.test import TestCase, Client
from django.urls import reverse


class HomeViewTest(TestCase):
    """首页视图测试"""

    def setUp(self):
        """测试前准备"""
        self.client = Client()

    def test_home_view_status_code(self):
        """测试首页视图状态码"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        """测试首页视图使用的模板"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "home/html/index.html")

    def test_home_view_context(self):
        """测试首页视图传递的上下文数据"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertIn("title", response.context)
        self.assertIn("description", response.context)
        self.assertEqual(response.context["title"], "Elepathy - 智慧共情的力量")
        self.assertEqual(
            response.context["description"],
            "通过强大的记忆力和深刻的情感理解力，提供智能、人性化、可靠的工具和服务。",
        )

    def test_home_view_content(self):
        """测试首页视图内容"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertContains(response, "智慧共情的力量")
        self.assertContains(response, "探索工具")
        self.assertContains(response, "了解更多")
        self.assertContains(response, "为什么选择 Elepathy?")
        self.assertContains(response, "强大记忆力")
        self.assertContains(response, "情感共鸣")

    def test_home_navigation_links(self):
        """测试首页导航链接"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertContains(response, '<a href="/" class="active">')
        self.assertContains(response, '<a href="/chat">')
        self.assertContains(response, '<a href="/tools">')
        self.assertContains(response, '<a href="/team">')

    def test_home_footer(self):
        """测试首页页脚"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertContains(
            response, "&copy; 2025 Elepathy Teams. All rights reserved."
        )


class HomeUrlsTest(TestCase):
    """首页URL测试"""

    def test_home_url_resolves(self):
        """测试首页URL解析"""
        url = reverse("home:home")
        self.assertEqual(url, "/")


class HomeStaticFilesTest(TestCase):
    """首页静态文件测试"""

    def setUp(self):
        self.client = Client()

    def test_home_css_loaded(self):
        """测试首页CSS文件加载"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertContains(
            response, '<link rel="stylesheet" href="/static/home/css/style.css">'
        )

    def test_home_js_loaded(self):
        """测试首页JS文件加载"""
        url = reverse("home:home")
        response = self.client.get(url)
        self.assertContains(response, '<script src="/static/home/js/main.js"></script>')
