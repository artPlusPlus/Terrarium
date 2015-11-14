import logging

from .._resource_types import RuntimeProfile
from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class RuntimeProfileManager(ResourceManager):
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
        return cls._get_resource(name)

    @classmethod
    def update_runtime_profile(cls, name, new_name=None, new_app=None, new_environment=None,
                               new_cmd_args=None, new_cmd_kwargs=None, new_description=None):
        update_kwargs = {}
        if new_name is not None:
            update_kwargs['name'] = new_name
        if new_app is not None:
            update_kwargs['app'] = new_app
        if new_environment is not None:
            update_kwargs['environment'] = new_environment
        if new_cmd_args is not None:
            update_kwargs['arguments'] = new_cmd_args
        if new_cmd_kwargs is not None:
            update_kwargs['keyword_arguments'] = new_cmd_kwargs
        if new_description is not None:
            update_kwargs['description'] = new_description
        super(RuntimeProfileManager, cls)._update_resource(name, **update_kwargs)

    @classmethod
    def delete_runtime_profile(cls, name):
        cls._delete_resource(name)

    @classmethod
    def find_runtime_profiles(cls, name_pattern=None):
        """
        Computes a list of all RuntimeProfile instances whose name matches the name_pattern expression

        Args:
            name_pattern (string): expression used by regex to match against App names.
        """
        attr_patterns = [('name', name_pattern)]
        result = cls._find_resources(attr_patterns)

        return result
