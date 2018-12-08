# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _
from django.conf import settings

MODELS = getattr(settings, 'PLUGSHOP_MODELS', {})
FORMS = getattr(settings, 'PLUGSHOP_FORMS', {})
CONFIG = getattr(settings, 'PLUGSHOP_CONFIG', {})
OPTIONS = getattr(settings, 'PLUGSHOP_OPTIONS', {})
MESSAGES = getattr(settings, 'PLUGSHOP_MESSAGES', {})

REQUEST_NAMESPACE = CONFIG.get('REQUEST_NAMESPACE', 'cart')
SESSION_NAMESPACE = CONFIG.get('SESSION_NAMESPACE', 'cart')
URL_PREFIX = CONFIG.get('URL_PREFIX', '')

STATUS_CHOICES = OPTIONS.get('STATUS_CHOICES', (
                            (1, _('Created')),
                            (2, _('Confirmed')),
                            (3, _('Denied')),
                            (4, _('Shipped')),
                            (5, _('Completed'))))
STATUS_CHOICES_START = STATUS_CHOICES[0][0]
STATUS_CHOICES_FINISH = STATUS_CHOICES[-1][0]

MESSAGE_SUCCESS = MESSAGES.get('SUCCESS', 'Order created')
MESSAGE_NEW_ORDER_USER = MESSAGES.get('NEW_ORDER_USER', 'New Order')
MESSAGE_NEW_ORDER_ADMIN = MESSAGES.get('NEW_ORDER_ADMIN', 'New Order')
