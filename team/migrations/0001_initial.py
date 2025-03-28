# Generated by Django 5.1.7 on 2025-03-28 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='姓名')),
                ('role', models.CharField(max_length=100, verbose_name='角色')),
                ('bio', models.TextField(blank=True, verbose_name='简介')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='邮箱')),
                ('avatar_path', models.CharField(blank=True, max_length=255, verbose_name='头像路径')),
                ('github_url', models.URLField(blank=True, verbose_name='GitHub 链接')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='排序')),
            ],
            options={
                'verbose_name': '团队成员',
                'verbose_name_plural': '团队成员',
                'ordering': ['order'],
            },
        ),
    ]
