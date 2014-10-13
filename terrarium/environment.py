# === IMPORTS ===
# Built-Ins
import os

# Third-Party

# External

# Internal


class Environment(object):
    """ Represents a Runtime Environment for an App. """

    _TOKENIZERS = (('%', '%'), ('$', ''), ('${', '}'))

    @property
    def name(self):
        return self._name

    @property
    def parent(self):
        return self._parent

    def __init__(self, name, parent=None):
        """ Instantiates a new Environment instance.

        :param name: A user-friendly name describing the environment.
        :param parent: An Environment instance from which this instance will
        inherit settings.
        :return: None
        """
        super(Environment, self).__init__()

        self._name = name
        self._parent = parent
        self._settings = {}

    def set_setting(self, name, value):
        """ Sets the value of an enivornment

        :param name: The name of the Environment Setting
        :param value: The value to associate with the named Setting
        :return: None
        """
        self._settings[name] = value

    def get_setting(self, name):
        """ Retrieves the value of a setting by its name

        :param name: The name of the Environment Setting
        :return: If a setting exists with the given name, the associated value is returned; otherwise, None.
        """
        try:
            return self._settings[name]
        except KeyError:
            if self._parent:
                return self._parent.get_setting(name)
        return None

    def expand(self, value, use_runtime_environment=True, overrides=None):
        """ Return 'value' with environment variables expanded.

        :param value: The object to expand
        :param use_runtime_environment:
        :param overrides:
        :return:
        """
        result = str(value)

        if overrides is None:
            overrides = {}

        expanding = True
        while expanding:
            expanding = False
            for setting_name, setting_value in self._settings.iteritems():
                try:
                    setting_value = overrides[setting_name]
                except KeyError:
                    pass
                for token_prefix, token_suffix in self._TOKENIZERS:
                    token = '{0}{1}{2}'.format(token_prefix, setting_name,
                                               token_suffix)
                    if token in result:
                        result = result.replace(token, setting_value)
                        expanding = True
                        break

        if use_runtime_environment:
            os.path.expandvars(result)

        return result

    def condense(self, value, use_runtime_environment=True, overrides=None):
        """ Return 'value' where environment variables replace matched values.

        :param value: Object to condense
        :param use_runtime_environment:
        :param overrides:
        :return:
        """
        pass