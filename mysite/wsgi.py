"""
==============================================================================
 * @FilePath: wsgi.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-24 17:53:13
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-25 22:48:47
 * @Copyright © 2025 WangWindow
 * @Descripttion: WSGI config for mysite project.
==============================================================================
It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
==============================================================================
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

application = get_wsgi_application()
