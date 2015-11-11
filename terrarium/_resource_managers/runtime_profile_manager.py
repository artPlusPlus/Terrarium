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
        try:
            profile = cls._resource_collection[name]
        except KeyError:
            msg = 'Update Failed: RuntimeProfile "{0}" not found.'.format(name)
            _LOG.error(msg)
            # TODO: Add ResourceNotFound error
            raise RuntimeError()

        _LOG.debug('Update Started: RuntimeProfile "{0}"'.format(name))

        orig_name = profile.name
        orig_app = profile.app
        orig_env = profile.environment
        orig_description = profile.description
        orig_args = profile.args
        orig_kwargs = profile.kwargs

        try:
            if new_name:
                msg = 'Updated RuntimeProfile "{0}": name from "{1}" to "{2}"'.format(
                    profile.name, orig_name, new_name)
                profile.name = new_name
                _LOG.debug(msg)

            if new_app:
                msg = 'Updated RuntimeProfile "{0}": app from "{1}" to "{2}"'.format(
                    profile.name, orig_app, new_app)
                profile.app = new_app
                _LOG.debug(msg)

            if new_environment:
                msg = 'Updated RuntimeProfile "{0}": environment from "{1}" to "{2}"'.format(
                    profile.name, orig_env, new_environment)
                profile.app = new_app
                _LOG.debug(msg)

            if new_description:
                msg = 'Updated RuntimeProfile "{0}": description'.format(profile.name)
                profile.description = new_description
                _LOG.debug(msg)

            if new_cmd_args:
                deleted_args = set(orig_args).difference(new_cmd_args)
                added_args = set(new_cmd_args).difference(orig_args)
                profile.arguments = new_cmd_args
                for arg in deleted_args:
                    msg = 'Updated RuntimeProfile "{0}": DEL arg "{1}"'.format(profile.name, arg)
                    _LOG.debug(msg)
                for arg in added_args:
                    msg = 'Updated RuntimeProfile "{0}": ADD arg "{0}"'.format(profile.name, arg)
                    _LOG.debug(msg)

            if new_cmd_kwargs:
                deleted_args = set(orig_kwargs.keys()).difference(new_cmd_kwargs.keys())
                added_args = set(new_cmd_kwargs.keys()).difference(orig_kwargs.keys())
                profile.keyword_arguments = new_cmd_kwargs
                for arg in deleted_args:
                    msg = 'Updated RuntimeProfile "{0}": DEL kwarg "{1}"'.format(profile.name, arg)
                    _LOG.debug(msg)
                for arg in added_args:
                    msg = 'Updated RuntimeProfile "{0}": ADD kwarg "{0}"'.format(profile.name, arg)
                    _LOG.debug(msg)
        except Exception as e:
            profile.name = orig_name
            profile.app = orig_app
            profile.environment = orig_env
            profile.description = orig_description
            profile.arguments = orig_args
            profile.keyword_arguments = orig_kwargs

            msg = 'Update Failed: RuntimeProfile "{0}" - {1}'.format(orig_name, e)
            _LOG.error(msg)

            # TODO: Add UpdateFailed error
            raise
        else:
            _LOG.debug('Update Complete: RuntimeProfile "{0}"'.format(orig_name))

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
