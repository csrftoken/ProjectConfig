#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import importlib


empty = object()

ENVIRONMENT_VARIABLE = "SETTINGS_MODULE"


def new_method_proxy(func):
    """
    新的方法代理
    """
    def inner(self, *args):
        if self._wrapped is empty:
            self._setup()
        return func(self._wrapped, *args)
    return inner


class ImproperlyConfigured(Exception):
    """
    不正确的配置
    """

    pass


class LazyObject(object):

    # 标识位(避免程序无限递归)
    _wrapped = None

    def __init__(self):
        self._wrapped = empty

    def _setup(self):
        raise NotImplementedError('subclasses of LazyObject must provide a _setup() method')

    def __setattr__(self, name, value):
        if name == "_wrapped":
            self.__dict__["_wrapped"] = value
        else:
            if self._wrapped is empty:
                self._setup()
            setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == "_wrapped":
            raise TypeError("can't delete _wrapped.")
        if self._wrapped is empty:
            self._setup()
        delattr(self._wrapped, name)

    __getattr__ = new_method_proxy(getattr)


class LazySettings(LazyObject):

    def _setup(self, name=None):

        settings_module = os.environ.get(ENVIRONMENT_VARIABLE)
        if not settings_module:
            desc = ("setting %s" % name) if name else "settings"
            raise ImproperlyConfigured(
                "Requested %s, but settings are not configured. "
                "You must either define the environment variable %s "
                "or call settings.configure() before accessing settings."
                % (desc, ENVIRONMENT_VARIABLE))

        self._wrapped = Settings(settings_module)


class Settings(object):

    def __init__(self, settings_module):

        self.SETTINGS_MODULE = settings_module

        mod = importlib.import_module(self.SETTINGS_MODULE)

        self._explicit_settings = set()

        for setting in dir(mod):
            if setting.isupper():
                setting_value = getattr(mod, setting)
                setattr(self, setting, setting_value)
                self._explicit_settings.add(setting)

    def is_overridden(self, setting):
        return setting in self._explicit_settings


settings = LazySettings()
