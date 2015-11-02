"""
Python version agnostic implementation of logging.NullHandler
"""
import logging

try:
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass
