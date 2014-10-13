"""

"""

# === IMPORTS ===
# Built-Ins

# Third-Party

# External

# Internal

 
class App(object):
    """ Data about an executable.

    """

    @property
    def name(self):
        return self._name

    @property
    def location(self):
        return self._location

    @property
    def executable(self):
        return self._executable

    @property
    def arguments(self):
        return self._arguments[:]

    def __init__(self, name):
        super(App, self).__init__()

        self._name = name
        self._location = None
        self._executable = None
        self._arguments = None