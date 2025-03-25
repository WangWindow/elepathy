"""
==============================================================================
 * @FilePath: manage.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-24 17:53:13
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-25 22:49:35
 * @Copyright © 2025 WangWindow
 * @Descripttion: Django's command-line utility for administrative tasks.
==============================================================================
"""

import os
import sys


def main():
    """
    Run administrative tasks.
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
