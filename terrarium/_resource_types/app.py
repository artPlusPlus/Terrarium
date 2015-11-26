class App(object):
    """
    Represents an executable application.

    Apps handle the path to an executable location. This path data is stored in two parts:
        - The ``location`` is the path to the directory containing the executable
        - The ``executable`` is he executable file name.
    """
    @property
    def name(self):
        """
        The name of the application.

        This may differ from the name of the executable and is meant to be user
        and UI friendly.

        Returns:
            The user/UI friendly name of the application as a string.
        """
        return self._name

    @name.setter
    def name(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._name = value
            else:
                raise ValueError('App name cannot be empty.')
        else:
            raise ValueError('App name must be a non-empty string.')

    @property
    def location(self):
        """
        The path up-to the executable.

        The location may contain environment variables.

        Returns:
            The compressed location of the Apps executable.
        """
        return self._location

    @location.setter
    def location(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._location = value
            else:
                raise ValueError('App location cannot be empty.')
        else:
            raise ValueError('App location must be a non-empty string.')

    @property
    def executable(self):
        """
        The name of the Apps executable.

        The executable may contain environment variables.

        Returns:
            The compressed executable name.
        """
        return self._executable

    @executable.setter
    def executable(self, value):
        if value:
            value = unicode(value).strip()
            if value:
                self._executable = value
            else:
                raise ValueError('App executable cannot be empty.')
        else:
            raise ValueError('App executable must be a non-empty string.')

    @property
    def description(self):
        """
        Description of the App.
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

    def __init__(self, name, location, executable, description=None):
        """
        Initializes an instance of an App.

        Args:
            name (basestring): User/UI friendly name for the App.
            location (basestring): Disk location of the Apps executable.
                Can contain environment variables.
            executable (basestring): Name of the Apps executable.
                Can contain environment variables.
        """
        super(App, self).__init__()

        self._name = None
        self._location = None
        self._executable = None
        self._description = None

        self.name = name
        self.location = location
        self.executable = executable
        self.description = description

    def __eq__(self, other):
        try:
            return all([self.location == other.location,
                        self.executable == other.executable])
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
