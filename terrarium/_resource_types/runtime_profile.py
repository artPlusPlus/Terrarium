import shlex
import logging


_LOG = logging.getLogger(__name__)


class RuntimeProfile(object):
    """
    A RuntimeProfile tightly couples an Environment, an App, and execution
    arguments.

    RuntimeProfile aims to encapsulate the details of executing an app in a
    specific environment with specific argumentation.
    """
    @property
    def name(self):
        """
        The name of the :class:`RuntimeProfile`.

        Meant to be User/UI friendly.

        Returns:
            The name of the :class:`RuntimeProfile` as a string.
        """
        return self._name

    @name.setter
    def name(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._name = value
            else:
                msg = 'RuntimeProfile name cannot be empty.'
                _LOG.error(msg)
                raise ValueError(msg)
        else:
            msg = 'RuntimeProfile name must be a non-empty string.'
            _LOG.error(msg)
            raise ValueError(msg)

    @property
    def app(self):
        """
        The name of an :class:`App`.

        The :class:`App` will be invoked with the ``arguments`` and
        ``keyword_arguments`` and have access to environment variables
        described in the :class:`Environment`.

        Returns:
            The name of the :class:`App` as a string.
        """
        return self._app

    @app.setter
    def app(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._app = value
            else:
                msg = 'RuntimeProfile App name cannot be empty.'
                _LOG.error(msg)
                raise ValueError(msg)
        else:
            msg = 'RuntimeProfile App name must be a non-empty string.'
            _LOG.error(msg)
            raise ValueError(msg)

    @property
    def environment(self):
        """
        The name of an :class:`Environment`.

        The :class:`Environment` describes the environment variable names and
        values to which the :class:`App` will have access to at runtime.

        Returns:
            The name of the :class:`Environment` as a string.
        """
        return self._environment

    @environment.setter
    def environment(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._environment = value
            else:
                msg = 'RuntimeProfile Environment name cannot be empty.'
                _LOG.error(msg)
                raise ValueError(msg)
        else:
            msg = 'RuntimeProfile Environment name must be a non-empty string.'
            _LOG.error(msg)
            raise ValueError(msg)

    @property
    def arguments(self):
        """
        Argumentation to be passed to the :class:`App`.

        Returns:
            A list of strings.
        """
        return self._args[:]

    @arguments.setter
    def arguments(self, value):
        self._args = []
        self._update_args(value)

    @property
    def keyword_arguments(self):
        """
        Keyword Argumentation to be passed to the :class:`App`.

        Returns:
            A dictionary of string keys and string values.
        """
        return self._kwargs.copy()

    @keyword_arguments.setter
    def keyword_arguments(self, value):
        self._kwargs.clear()
        self._update_kwargs(value)

    @property
    def description(self):
        """
        Description of the :class:`RuntimeProfile`.

        The description should provide a high-level understanding of how the
        :class:`App`, :class:`Environment`, and argumentation interact at
        runtime.

        Returns:
            The description as a string.
        """
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

    def __init__(self, name, app, environment, cmd_args=None, cmd_kwargs=None,
                 description=None):
        """
        Initializes a RuntimeProfile instance.

        Args:
            name (string): A User/UI friendly name
            app (string): Name of an existing App
            environment (string): Name of an existing Environment
            cmd_args (Optional[[string]]): Arguments to pass to the App
            cmd_kwargs (Optional[{string:string}]): Keyword Arguments to pass
                to the App
            description (Optional[string]): Describes the configuration and
                runtime state of the App at a high level.
        """
        self._name = name
        self._app = app
        self._environment = environment
        self._args = []
        self._kwargs = {}
        self._description = description

        self.name = name
        self.app = app
        self.environment = environment
        self.description = description
        self.arguments = cmd_args
        self.keyword_arguments = cmd_kwargs

    def _update_args(self, args):
        if isinstance(args, basestring):
            args = shlex.split(args)
        args = [unicode(v).strip() for v in args]

        added_args = set(args).difference(self._args)
        dropped_args = set(self._args).difference(args)

        self._args.extend(added_args)
        for arg in added_args:
            msg = 'Updated {0} "{1}": ADD arg "{2}"'.format(
                self.__class__.__name__, self.name, arg)
            _LOG.debug(msg)

        self._args = [a for a in self._args if a not in dropped_args]
        for arg in dropped_args:
            msg = 'Updated {0} "{1}": REM arg "{2}"'.format(
                self.__class__.__name__, self.name, arg)
            _LOG.debug(msg)

    def _update_kwargs(self, kwargs):
        if isinstance(kwargs, basestring):
            kwargs = shlex.split(kwargs)

        _kwargs = {}
        try:
            _kwargs.update(kwargs)
        except AttributeError:
            for kw, arg in kwargs:
                _kwargs[kw] = arg
        for kw, _val in _kwargs.iteritems():
            _kw = unicode(kw).strip()
            if _val:
                _val = unicode(_val).strip()
            del _kwargs[kw]
            _kwargs[_kw] = _val

        added_args = set(_kwargs.keys()).difference(self._kwargs.keys())
        modded_args = set(self._kwargs.keys()).intersection(_kwargs.keys())
        dropped_args = set(self._kwargs.keys()).difference(_kwargs.keys())
        dropped_args.update([kw for kw, val in _kwargs.iteritems() if not val])

        for kw, arg in zip(added_args, [_kwargs[kw] for kw in added_args]):
            self._kwargs[kw] = arg
            msg = 'Updated {0} "{1}": ADD kwarg "{2}" - "{3}"'.format(
                self.__class__.__name__, self.name, kw, arg)
            _LOG.debug(msg)

        for kw, arg in zip(modded_args, [_kwargs[kw] for kw in modded_args]):
            if self._kwargs[kw] == arg:
                continue
            self._kwargs[kw] = arg
            msg = 'Updated {0} "{1}": MOD kwarg "{2}" - "{3}"'.format(
                self.__class__.__name__, self.name, kw, arg)
            _LOG.debug(msg)

        for kw in dropped_args:
            del self._kwargs[kw]
            msg = 'Updated {0} "{0}": REM kwarg "{2}"'.format(
                self.__class__.__name__, self.name, kw)
            _LOG.debug(msg)

    def __eq__(self, other):
        try:
            return all([self.name == other.name,
                        self.app == other.app,
                        self.environment == other.environment,
                        self.arguments == other.arguments])
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
