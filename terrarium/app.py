import os
import weakref


class App(object):
    """ Represents an executable application. """
    _apps = weakref.WeakSet()

    @property
    def name(self):
        """
        The name of the application.

        This may differ from the name of the executable and is meant to be
        user and UI friendly.

        Returns:
            The user/UI friendly name of the application as a string.
        """
        return self._name

    @property
    def location(self):
        """
        The path up-to the executable.

        The location may contain environment variables.

        Returns:
            The compressed location of the Apps executable.
        """
        return self._location

    @property
    def executable(self):
        """
        The name of the Apps executable.

        The executable may contain environment variables.

        Returns:
            The compressed executable name.
        """
        return self._executable

    def __init__(self, name, location, executable):
        """
        Initializes an instance of an App.

        Args:
            name (str): User/UI friendly name for the App.
            location (str): Disk location of the Apps executable.
                Can contain environment variables.
            executable (str): Name of the Apps executable.
                Can contain environment variables.
        """
        super(App, self).__init__()

        self._name = name
        self._location = location
        self._executable = executable

        self.__class__._apps.add(self)

    def __eq__(self, other):
        my_raw_path = os.path.join(self.location, self.executable)
        try:
            other_raw_path = os.path.join(other.location, other.executable)
            return my_raw_path == other_raw_path
        except AttributeError:
            pass
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @classmethod
    def all_apps(cls):
        """
        Provides a set containing all known App instances.

        Return:
            A set of App instances.
        """
        result = set()
        result.update(cls._apps)
        return result

    def resolve_path(self, environment, use_runtime=True):
        """
        Resolves the path of the App using the provided environment.

        Args:
            environment (terrarium.Environment): This environment will be used
                to resolve environment variables found in the Apps location
                and name.
            use_runtime (bool): If true, the process runtime will be used to
                further resolve any environment variables not handled by the
                terrarium.Environment instance.

        Return:
            A string with all understood environment variables resolved.
        """
        location = environment.expand(self._location,
                                      use_runtime_environment=use_runtime)
        executable = environment.expand(self._executable,
                                        use_runtime_environment=use_runtime)

        return os.path.normpath(os.path.join(location, executable))
