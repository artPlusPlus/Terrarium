import os
import re


_VAR_PATTERN = re.compile(r'([%$]\{*(?P<var>\w*)[%}]?)')
_VAR_FORMATS = ('%{0}%'.format,
                '${0}'.format,
                '${{{0}}}'.format)
_INTERNAL_VAR_PATTERN = re.compile(r'(@\[(?P<var>\w*)\]@)')
_INTERNAL_VAR_FORMAT = '@[{0}]@'.format


class Environment(object):
    """
    Represents a Runtime Environment for an App.

    Environments hold environment variable data and can be structured hierarchically.
    They have the ability to expand and compress values based on the variable data
    available to themselves and hierarchical their ancestors.
    """
    @property
    def name(self):
        """
        The name of the Environment.

        Meant to be User/UI friendly.

        Returns:
            The name of the Environment as a string.
        """
        return self._name

    @name.setter
    def name(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._name = value
            else:
                raise ValueError('Environment name cannot be empty.')
        else:
            raise ValueError('Environment name must be a non-empty string.')

    @property
    def parent(self):
        """
        The name of the parent Environment.

        When resolving variables, the Environment will first look at its own data.
        If the variable is not found, it will look up to its parent. This will repeat
        until the variable is resolved or an Environment is reached that has no parent.

        Returns:
            The name of the parent Environment or None.
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._parent = value
            else:
                raise ValueError('Environment parent cannot be empty.')
        else:
            raise ValueError('Environment parent must be a non-empty string.')

    @property
    def description(self):
        """
        Description of the Environment.

        The description should offer a high-level view of the variables and intended usage.

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

    @property
    def variables(self):
        """
        The variables defined by the environment.

        Variables defined in parent scopes are not included.
        Variables are in their original form.

        Returns:
            A dictionary with variable name keys and variable value values.
        """
        return self._vars.copy()

    def __init__(self, name, parent=None, description=None):
        """
        Instantiates a new Environment instance.

        Args:
            name (str): A User/UI friendly name.
            parent (str): The name of an existing Environment
            description (str): A User/UI friendly description.

        Returns:
            None
        """
        super(Environment, self).__init__()

        self._name = None
        self._parent = None
        self._description = None
        self._vars = {}

        self.name = name
        self.parent = parent
        self.description = description

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

    def _set_var(self, name, value):
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

    def _get_var(self, name):
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
                return self._parent.get_var(name)
        return None

    def iterkeys(self):
        return self._vars.iterkeys()

    def itervalues(self):
        for name in self._vars:
            yield self.expand(self._get_var(name))

    def iteritems(self):
        for name, value in self._vars.iteritems():
            yield (name, self.expand(self._get_var(name)))

    def update(self, other, **kwargs):
        try:
            names = other.keys()
        except AttributeError:
            for name, value in other:
                self._set_var(name, value)
        else:
            for name in names:
                self._set_var(name, other[name])

    def __len__(self):
        return len(self._vars)

    def __getitem__(self, name):
        value = self._get_var(name)
        if value is None:
            raise KeyError('Variable "{0}" not found.'.format(name))
        return value

    def __setitem__(self, name, value):
        self._set_var(name, value)

    def __delitem__(self, name):
        del self._vars[name]

    def __iter__(self):
        return self._vars.iterkeys()

    def __contains__(self, name):
        return self._get_var(name) is not None

    def __eq__(self, other):
        try:
            return all([self.name == other.name,
                        self.parent == other.parent,
                        self.variables == other.variables])
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
