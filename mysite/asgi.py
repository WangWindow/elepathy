"""
==============================================================================
 * @FilePath: asgi.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-24 17:53:13
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-25 22:48:20
 * @Copyright © 2025 WangWindow
 * @Descripttion: ASGI config for mysite project.
==============================================================================
It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
==============================================================================
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_asgi_application()
