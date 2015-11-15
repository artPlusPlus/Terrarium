import logging

from .._resource_types import Environment
from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class EnvironmentManager(ResourceManager):
    """
    EnvironmentManager provides CRUD-L services for Environment data.
    """
    _resource_type = Environment
    _resource_collection = {}

    @classmethod
    def create_environment(cls, name, parent=None, variables=None, description=None):
        return cls._create_resource(name, parent=parent, variables=variables, description=description)

    @classmethod
    def get_environment(cls, name):
        return cls._get_resource(name)

    @classmethod
    def update_environment(cls, name, new_name=None, new_description=None, new_parent=None, update_variables=None):
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
        cls._delete_resource(name)

    @classmethod
    def find_environments(cls, name_pattern=None):
        attr_patterns = [('name', name_pattern)]
        result = cls._find_resources(attr_patterns)

        return result
