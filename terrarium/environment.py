import os
import re
import weakref


_VAR_PATTERN = re.compile(r'([%$]\{*(?P<var>\w*)[%}]?)')
_VAR_FORMATS = ('%{0}%'.format,
                '${0}'.format,
                '${{{0}}}'.format)
_INTERNAL_VAR_PATTERN = re.compile(r'(@\[(?P<var>\w*)\]@)')
_INTERNAL_VAR_FORMAT = '@[{0}]@'.format


class Environment(object):
    """ Represents a Runtime Environment for an App. """
    _environments = weakref.WeakSet()

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    def __init__(self, name, parent=None):
        """
        Instantiates a new Environment instance.

        Args:
            name (str): A user-friendly name describing the environment.
            parent (Environment): An :class:`Environment` instance from which
                this instance will inherit settings.

        Returns:
            None
        """
        super(Environment, self).__init__()

        self._name = name
        self._parent = parent
        self._vars = {}

        self.__class__._environments.add(self)

    @classmethod
    def all_environments(cls):
        result = set()
        result.update(cls._environments)
        return result

    def set_var(self, name, value):
        """
        Sets the value of an Environment variable

        Args:
            name (str): The name of the Environment Setting
            value (str): The value to associate with the named Setting

        Returns:
            None
        """
        value = str(value)
        if not value:
            msg = "Error setting {0}: Value cannot be empty.".format(name)
            raise ValueError(msg)
        while True:
            match = _VAR_PATTERN.search(value)
            if not match:
                break
            value = value.replace(
                match.group(0), _INTERNAL_VAR_FORMAT(match.group('var')))
        self._vars[name] = os.path.normpath(value)

    def get_setting(self, name):
        """
        Resolves the given name with an assigned value.

        Args:
            name (str): The name of the Environment Setting

        Returns:
            A string if a setting exists with the given name; otherwise, None.
        """
        try:
            return self._vars[name]
        except KeyError:
            if self._parent:
                return self._parent.get_setting(name)
        return None

    def expand(self, value, var_format=None, use_runtime_environment=True,
               overrides=None):
        """
        Replaces environment variable names with appropriate values.

        Substrings of the following forms are replaced by the value of
            environment variable *name*:
            * name
            * ${name}
            * %name%

        Args:
            value (str): A string containing environment variables.
            var_format (str): String format expression used to generate a
                variables final output form.
                Example: '%{0}%'
            use_runtime_environment (bool): If true, once the Environment
                instance has resolved all the variables it can, the runtime
                environment is invoked to resolve any remaining variables.
            overrides ({str:str}): Mapping of environment variable names and
                values. If a variable name key matches an environment variable
                defined in the Environment instance, the value from the
                override map is used. If an override has no match in the
                Environment instance, it will not be used at all.

        Return:
            The argument with environment variables expanded.
        """
        value = os.path.normpath(value)

        result = str(value)

        if not overrides:
            overrides = {}

        if not var_format:
            var_format = '%{0}%'.format
        elif isinstance(var_format, basestring):
            var_format = str(var_format).format

        expanding = True
        while expanding:
            expanding = False
            for match in _VAR_PATTERN.finditer(result):
                var, var_name = match.groups()
                try:
                    value = overrides[var_name]
                except KeyError:
                    try:
                        value = self._vars[var_name]
                    except KeyError:
                        continue
                result = result.replace(var, value)
                expanding = True
            for match in _INTERNAL_VAR_PATTERN.findall(result):
                var, var_name = match
                result = result.replace(var, self._vars[var_name])
                expanding = True

        expanding = True
        while expanding:
            expanding = False
            for match in _INTERNAL_VAR_PATTERN.finditer(result):
                var, var_name = match.groups()
                result = result.replace(var, var_format(var_name))
                expanding = True

        while use_runtime_environment:
            r = os.path.expandvars(result)
            use_runtime_environment = r != result
            result = r

        return os.path.normpath(result)

    def compress(self, value, var_format=None, use_runtime_environment=True,
                 overrides=None):
        """
        Replaces environment variable values with environment variable names.

        Compression works by inserting variables for the largest,
        non-overlapping value matches.

        Args:
            value (str): Object to condense
            var_format (str): String format expression used to generate a
                variables final output form.
                Example: '%{0}%'
            use_runtime_environment (bool): If true, once the Environment
                instance has resolved all the variables it can, the runtime
                environment is invoked to resolve any remaining variables.
            overrides ({str:str}): Mapping of environment variable names and
                values. If a variable name key matches an environment variable
                defined in the Environment instance, the value from the
                override map is used. If an override has no match in the
                Environment instance, it will not be used at all.

        Return:
            The argument with environment variables condensed.
        """
        value = os.path.normpath(value)

        result = str(value)

        if not var_format:
            var_format = '%{0}%'.format
        elif isinstance(var_format, basestring):
            var_format = str(var_format).format

        if not overrides:
            overrides = {}

        expanded_vars = {}

        for name, value in self._vars.iteritems():
            expanded_vars[name] = self.expand(
                value, overrides=overrides,
                use_runtime_environment=use_runtime_environment)

        if use_runtime_environment:
            for name, value in os.environ.iteritems():
                expanded_vars[name] = self.expand(value, overrides=overrides,
                                                  use_runtime_environment=True)

        sorted_var_names = sorted(
            expanded_vars, reverse=True,
            key=lambda vn: len(expanded_vars[vn]))

        while not expanded_vars[sorted_var_names[-1]]:
            del expanded_vars[sorted_var_names.pop()]

        compressing = True
        while compressing:
            compressing = False
            for var_name in sorted_var_names:
                if expanded_vars[var_name] in result:
                    result = result.replace(expanded_vars[var_name],
                                            var_format(var_name))
                    compressing = True
                    break

        return os.path.normpath(result)

    def apply(self, overrides=None):
        """
        Pushes the Environment instance's variable data into the current
            runtime environment

        Args:
            overrides ({str:str}): Mapping of environment variable names and
                values. If a variable name key matches an environment variable
                defined in the Environment instance, the value from the
                override map is used. If an override has no match in the
                Environment instance, it will not be used at all.

        Return:
            None
        """
        if not overrides:
            overrides = {}

        for name, value in self._vars.iteritems():
            if name in overrides:
                value = overrides[name]
            os.environ[name] = value
