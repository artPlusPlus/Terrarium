import logging

from .._resource_types import RuntimeProfile
from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class RuntimeProfileManager(ResourceManager):
    """
    class::`RuntimeProfileManager` provides CRUD-L services for class::`RuntimeProfile` data.
    """
    _resource_type = RuntimeProfile
    _resource_collection = {}

    @classmethod
    def create_runtime_profile(cls, name, app, environment, cmd_args=None,
                               cmd_kwargs=None, description=None):
        profile = cls._create_resource(name, app, environment, cmd_args=cmd_args,
                                       cmd_kwargs=cmd_kwargs, description=description)
        return profile

    @classmethod
    def get_runtime_profile(cls, name):
        """
        Attempts to retrieve an class::`RuntimeProfile` that matches the ``name`` argument exactly.

        Args:
            name: The name of an existing class::`RuntimeProfile`.

        Returns:
            class::`RuntimeProfile` instance or None if no class::`RuntimeProfile` is found matching ``name``.
        """
        return cls._get_resource(name)

    @classmethod
    def update_runtime_profile(cls, name, new_name=None, new_description=None, new_app=None, new_environment=None,
                               new_cmd_args=None, new_cmd_kwargs=None):
        """
        Update an existing class::`RuntimeProfile`.

        Each call to ``update_runtime_profile`` is transactional. If any part of the update fails, the entire update
        will fail.

        Args:
            name (basestring): Name of an existing class::`RuntimeProfile`.
            new_name (basestring): New name for the class::`RuntimeProfile`.
            new_description (basestring): New description for the class::`RuntimeProfile`.
            new_app (basestring): Name of an existing class::`App`.
            new_environment (basestring): Name of an existing class::`Environment`.
            new_cmd_args (list(basestring)): Arguments to be passed to the App executable.
            new_cmd_kwargs (dict(basestring: basestring)): Keyword Arguments to be passed to the App executable.
        """
        update_kwargs = {}
        if new_name is not None:
            update_kwargs['name'] = new_name
        if new_description is not None:
            update_kwargs['description'] = new_description
        if new_app is not None:
            update_kwargs['app'] = new_app
        if new_environment is not None:
            update_kwargs['environment'] = new_environment
        if new_cmd_args is not None:
            update_kwargs['arguments'] = new_cmd_args
        if new_cmd_kwargs is not None:
            update_kwargs['keyword_arguments'] = new_cmd_kwargs
        super(RuntimeProfileManager, cls)._update_resource(name, **update_kwargs)

    @classmethod
    def delete_runtime_profile(cls, name):
        """
        Remove all data describing an class::`RuntimeProfile`

        Args:
            name (basestring): Name of an existing class::`RuntimeProfile`.
        """
        cls._delete_resource(name)

    @classmethod
    def find_runtime_profiles(cls, name_pattern=None):
        """
        Computes a list of all managed class::`RuntimeProfile` instances matching various criteria.

        Args:
            name_pattern (basestring): Used to regex match profile names.

        Returns:
            List[class::`RuntimeProfile`]
        """
        attr_patterns = [('name', name_pattern)]
        result = cls._find_resources(attr_patterns)

        return result
