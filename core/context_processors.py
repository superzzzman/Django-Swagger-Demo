# coding=utf-8

import logging
import datetime
import hashlib

from django.conf import settings as _settings

log = logging.getLogger(__name__)


def settings(request):
    """
    TEMPLATE_CONTEXT_PROCESSORS
    """
    context = {'settings': _settings}
    return context
