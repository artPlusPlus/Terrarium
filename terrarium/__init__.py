""" Creates hospitable runtime environments for apps.

.. moduleauthor:: Matt Robinson <matt@technicalartisan.com>

"""
import logging
from ._null_handler import NullHandler

from .app import App
from .environment import Environment
from .runtime_profile import RuntimeProfile

from .manager import Manager


_LOG = logging.getLogger(__name__)
_LOG.addHandler(NullHandler)

_G_MANAGER = Manager()
