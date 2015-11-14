import shlex
import logging


_LOG = logging.getLogger(__name__)


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
        self._update_args(value)

    @property
    def keyword_arguments(self):
        return self._kwargs.copy()

    @keyword_arguments.setter
    def keyword_arguments(self, value):
        self._update_kwargs(value)

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
        self._args = []
        self._kwargs = {}
        self._description = description

        self._update_args(cmd_args)
        self._update_kwargs(cmd_kwargs)

    def _update_args(self, args):
        if isinstance(args, basestring):
            args = shlex.split(args)
        args = [unicode(v).strip() for v in args]

        added_args = set(args).difference(self._args)
        dropped_args = set(self._args).difference(args)

        self._args.extend(added_args)
        for arg in added_args:
            msg = 'Updated {0} "{1}": ADD arg "{2}"'.format(self.__class__.__name__, self.name, arg)
            _LOG.debug(msg)

        self._args = [a for a in self._args if a not in dropped_args]
        for arg in dropped_args:
            msg = 'Updated {0} "{1}": REM arg "{2}"'.format(self.__class__.__name__, self.name, arg)
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

        added_args = [unicode(kw).strip() for kw in set(_kwargs.keys()).difference(self._kwargs.keys())]
        modded_args = [unicode(kw).strip() for kw in set(self._kwargs.keys()).intersection(_kwargs.keys())]
        dropped_args = [unicode(kw).strip() for kw in set(self._kwargs.keys()).difference(_kwargs.keys())]
        dropped_args.extend(kw for kw, val in _kwargs.iteritems() if not val or not unicode(val).strip())

        for kw, arg in zip(added_args, [unicode(kwargs[kw]).strip() for kw in added_args]):
            self._kwargs[kw] = arg
            msg = 'Updated {0} "{1}": ADD kwarg "{2}" - "{3}"'.format(self.__class__.__name__, self.name, kw, arg)
            _LOG.debug(msg)

        for kw, arg in zip(modded_args, [unicode(kwargs[kw]).strip() for kw in modded_args]):
            if self._kwargs[kw] == arg:
                continue
            self._kwargs[kw] = arg
            msg = 'Updated {0} "{1}": MOD kwarg "{2}" - "{3}"'.format(self.__class__.__name__, self.name, kw, arg)
            _LOG.debug(msg)

        for kw in dropped_args:
            del self._kwargs[kw]
            msg = 'Updated {0} "{0}": REM kwarg "{2}"'.format(self.__class__.__name__, self.name, kw)
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
