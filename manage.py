#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os

# 获取项目目录名称
PROJECT_NAME = os.path.basename(os.path.dirname(os.path.abspath(os.path.realpath(__file__))))


if __name__ == '__main__':
    os.environ.setdefault("SETTINGS_MODULE", "{}.settings".format(PROJECT_NAME))

    try:
        from conf import settings

        print(settings.DEBUG)

        print(settings.BAES_DIR)

    except ImportError:
        pass
