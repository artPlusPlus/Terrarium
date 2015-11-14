"""Hospitable runtime environments for applications.

Author:
    Matt Robinson <matt@technicalartisan.com>

"""
import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

from ._resource_types import *
from ._resource_managers import *
from ._util import *
from ._errors import *

_LOG = logging.getLogger(__name__)
_LOG.addHandler(NullHandler())

