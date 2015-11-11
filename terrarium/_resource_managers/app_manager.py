import logging

from .._resource_types import App
from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class AppManager(ResourceManager):
    """
    AppManager provides CRUD-L services for App data.
    """
    _resource_type = App
    _resource_collection = {}

    @classmethod
    def create_app(cls, name, location, executable, description=None):
        """
        Attempts to create a new App instance.

        Args:
            name (basestring): The name of the App. This must be unique among App instances.
            location (basestring): Directory path containing an executable named ``executable``
            executable (basestring): Filename of an executable
            description (Optional[basestring]): Human readable description of the App.

        Returns:
            A new class::`App` instance
        """
        return cls._create_resource(name, location, executable, description=description)

    @classmethod
    def get_app(cls, name):
        """
        Attempts to retrieve an App that matches the 'name' argument exactly.

        Args:
            name: The name of an existing App.

        Returns:
            class::`App` instance or None if no class::`App` is found matching ``name``.
        """
        return cls._get_resource(name)

    @classmethod
    def update_app(cls, name, new_name=None, new_location=None, new_executable=None, new_description=None):
        """
        Update an existing class::`App`.

        Each call to update_app is transactional. If any part of the update fails, the entire update will fail.

        Args:
            name (basestring): Name of an existing App.
            new_name (basestring): New name for the App.
            new_location (basestring): New path to the directory containing the executable.
            new_executable (basestring): New filename of the executable.
            new_description (basestring): New description for the App.
        """
        try:
            app = cls._resource_collection[name]
        except KeyError:
            msg = 'Update Failed: App "{0}" not found.'.format(name)
            _LOG.error(msg)
            # TODO: Add UpdateFailed error
            raise

        _LOG.debug('Update Started: App "{0}"'.format(name))

        orig_name = app.name
        orig_location = app.location
        orig_executable = app.executable
        orig_description = app.description

        try:
            if new_name:
                msg = 'Updated App "{0}": name "{1}"'.format(app.name, new_name)
                app.name = new_name
                _LOG.debug(msg)

            if new_location:
                msg = 'Updated App "{0}": location "{1}"'.format(app.name, new_location)
                app.location = new_location
                _LOG.debug(msg)

            if new_executable:
                msg = 'Updated App "{0}": executable "{1}"'.format(app.name, new_executable)
                app.executable = new_executable
                _LOG.debug(msg)

            if new_description:
                msg = 'Updated App "{0}": description'.format(app.name, new_description)
                app.description = new_description
                _LOG.debug(msg)
        except Exception as e:
            app.name = orig_name
            app.location = orig_location
            app.executable = orig_executable
            app.description = orig_description

            msg = 'Update Failed: App "{0}" - {1}'.format(orig_name, e)
            _LOG.error(msg)

            # TODO: Add UpdateFailed error
            raise
        else:
            _LOG.debug('Update Complete: App "{0}"'.format(name))

    @classmethod
    def delete_app(cls, name):
        """
        Remove all data about an App

        Args:
            name (basestring): Name of an existing App.
        """
        cls._delete_resource(name)

    @classmethod
    def find_apps(cls, name_pattern=None):
        """
        Computes a list of all managed App instances whose name matches the name_pattern expression

        Args:
            name_pattern (basestring): expression used by regex to match against App names.

        Returns:
            List[class::`App`]
        """
        attr_patterns = [('name', name_pattern)]
        result = cls._find_resources(attr_patterns)

        return result
