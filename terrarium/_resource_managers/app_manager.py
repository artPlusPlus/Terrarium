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
    def update_app(cls, name, new_name=None, new_description=None, new_location=None, new_executable=None):
        """
        Update an existing class::`App`.

        Each call to update_app is transactional. If any part of the update fails, the entire update will fail.

        Args:
            name (basestring): Name of an existing App.
            new_name (basestring): New name for the App.
            new_description (basestring): New description for the App.
            new_location (basestring): New path to the directory containing the executable.
            new_executable (basestring): New filename of the executable.
        """
        update_kwargs = {}
        if new_name is not None:
            update_kwargs['name'] = new_name
        if new_description is not None:
            update_kwargs['description'] = new_description
        if new_location is not None:
            update_kwargs['location'] = new_location
        if new_executable is not None:
            update_kwargs['executable'] = new_executable
        super(AppManager, cls)._update_resource(name, **update_kwargs)

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
