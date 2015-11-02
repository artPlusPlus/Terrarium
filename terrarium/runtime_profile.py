import os
import shlex

from .environment import Environment
from .app import App


class RuntimeProfile(object):
    """
    A RuntimeProfile tightly couples an Environment, an App, and execution arguments.

    RuntimeProfile aims to encapsulate the details of executing an app in a specific
    environment with specific argumentation.
    """
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._name = value
            else:
                raise ValueError('RuntimeProfile name cannot be empty.')
        else:
            raise ValueError('RuntimeProfile name must be a non-empty string.')

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._app = value
            else:
                raise ValueError('RuntimeProfile App name cannot be empty.')
        else:
            raise ValueError('RuntimeProfile App name must be a non-empty string.')

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._environment = value
            else:
                raise ValueError('RuntimeProfile Environment name cannot be empty.')
        else:
            raise ValueError('RuntimeProfile Environment name must be a non-empty string.')

    @property
    def arguments(self):
        return self._args[:]

    @arguments.setter
    def arguments(self, value):
        value = shlex.split(value)
        value = [unicode(v).strip() for v in value]
        self._args = value

    @property
    def keyword_arguments(self):
        return self._kwargs.copy()

    @keyword_arguments.setter
    def keyword_arguments(self, value):
        _value = {}
        for keyword, arg in value:
            keyword = unicode(keyword).strip()
            arg = unicode(arg).strip()
            _value[keyword] = arg
        self._kwargs = _value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if value:
            value = unicode(value).strip()
            if not value:
                value = None
        else:
            value = None
        self._description = value

    def __init__(self, name, app, environment, cmd_args=None, cmd_kwargs=None, description=None):
        """
        Initializes a RuntimeProfile instance.

        Args:
            name (string): A User/UI friendly name
            app (string): Name of an existing App
            environment (string): Name of an existing Environment
            cmd_args (Optional[[string]]): Arguments to pass to the App
            cmd_kwargs (Optional[{string:string}]): Keyword Arguments to pass to the App
            description (Optional[string]): Describes the configuration and runtime state of the App at a high level.
        """
        self._name = name
        self._app = app
        self._environment = environment
        self._args = cmd_args or []
        self._kwargs = cmd_kwargs or {}
        self._description = description

    def __eq__(self, other):
        try:
            return all([self.app == other.app,
                        self.environment == other.environment,
                        self.arguments == other.arguments])
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
