"""
==============================================================================
 * @FilePath: main.py
 * @Author: WangWindow 1598593280@qq.com
 * @Date: 2025-03-24 17:13:57
 * @LastEditors: WangWindow 1598593280@qq.com
 * @LastEditTime: 2025-03-24 22:33:34
 * @Copyright © 2025 WangWindow
 * @Descripttion: Entry Point
==============================================================================
"""

import os
import subprocess
import sys


def main():
    run_django_server()


def run_django_server():
    """
    Run Django server using manage.py
    """
    print("Start Django server...")
    try:
        # Check if manage.py exists
        if os.path.exists("manage.py"):
            manage_py_path = "manage.py"
        else:
            print("Not found manage.py")
            return False

        # Build and Run the command
        cmd = [sys.executable, manage_py_path, "runserver"]
        print(f"Running: {' '.join(cmd)}")

        # Start the process
        process = subprocess.Popen(cmd)

        # Wait for the process to finish
        process.wait()
        return process.returncode == 0

    except Exception as e:
        print(f"Start Django server failed: {e}")
        return False


if __name__ == "__main__":
    main()
