import logging

from .._resource_types import Environment
from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class EnvironmentManager(ResourceManager):
    """
    :class:`EnvironmentManager` provides CRUD-L services for
    :class:`Environment` data.
    """
    _resource_type = Environment
    _resource_collection = {}

    @classmethod
    def create_environment(cls, name, description=None, parent=None,
                           variables=None):
        """
        Attempts to create a new Environment instance.

        Any Environments created through the EnvironmentManager are managed by
        the EnvironmentManager.

        Args:
            name (basestring): Name for the :class:`Environment`. Must be
                unique relative to other managed :class:`Environment` instances.
            description: User-friendly description of the environment.
            parent (Optional[basestring]): Name of another
                :class:`Environment`. Defaults to None.
            variables (dict): Key value pairs describing environment variables
                and their values

        Returns:
            An :class:`Environment` instance.
        """
        return cls._create_resource(name, parent=parent, variables=variables,
                                    description=description)

    @classmethod
    def get_environment(cls, name):
        """
        Attempts to retrieve an :class:`Environment` that matches the ``name``
        argument exactly.

        Args:
            name: The name of an existing :class:`Environment`.

        Returns:
            :class:`Environment` instance or None if no :class:`Environment` is
                found matching ``name``.
        """
        return cls._get_resource(name)

    @classmethod
    def update_environment(cls, name, new_name=None, new_description=None,
                           new_parent=None, update_variables=None):
        """
        Update an existing :class:`Environment`.

        Each call to update_environment is transactional. If any part of the
            update fails, the entire update will fail.

        Args:
            name (basestring): Name of an existing Environment.
            new_name (basestring): New name for the Environment.
            new_description (basestring): New description for the Environment.
            new_parent (basestring): Name of an existing Environment.
            update_variables (basestring): New key-value pairs representing
                environment variable names and values.
        """
        update_kwargs = {}
        if new_name is not None:
            update_kwargs['name'] = new_name
        if new_description is not None:
            update_kwargs['description'] = new_description
        if new_parent is not None:
            update_kwargs['parent'] = new_parent
        if update_variables is not None:
            update_kwargs['variables'] = update_variables
        super(EnvironmentManager, cls)._update_resource(name, **update_kwargs)

    @classmethod
    def delete_environment(cls, name):
        """
        Remove all data describing an :class:Environment`

        Args:
            name (basestring): Name of an existing :class:`Environment`.
        """
        cls._delete_resource(name)

    @classmethod
    def find_environments(cls, name_pattern=None):
        """
        Computes a list of all managed :class:`Environment` instances matching
        various criteria.

        Args:
            name_pattern (basestring): Used to regex match Environment names.

        Returns:
            List[:class:`Environment`]
        """
        attr_patterns = [('name', name_pattern)]
        result = cls._find_resources(attr_patterns)

        return result
