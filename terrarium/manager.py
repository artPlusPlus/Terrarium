import operator
import re
import logging

from .app import App
from .environment import Environment
from .runtime_profile import RuntimeProfile


_LOG = logging.getLogger(__name__)


class Manager(object):
    def __init__(self):
        self._apps = {}
        self._environments = {}
        self._profiles = {}

    def create_app(self, name, location, executable, description=None):
        app = self._create_resource(App, self._apps, name, location, executable, description=description)
        return app

    def get_app(self, name):
        return self._get_resource(name, self._apps)

    def update_app(self, name, new_name=None, new_location=None, new_executable=None, new_description=None):
        try:
            app = self._apps[name]
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

    def delete_app(self, name):
        self._delete_resource(name, self._apps)

    def find_apps(self, name_pattern=None):
        """
        Computes a list of all managed App instances whose name matches the name_pattern expression

        Args:
            name_pattern (string): expression used by regex to match against App names.
        """
        attr_patterns = [('name', name_pattern)]
        result = self._find_resources(attr_patterns, [self._apps])

        return result

    def create_environment(self, name, parent, description=None):
        env = self._create_resource(Environment, self._environments, name, parent, description=description)
        return env

    def get_environment(self, name):
        return self._get_resource(name, self._environments)

    def update_environment(self, name, new_name=None, new_parent=None, new_description=None, update_variables=None):
        try:
            env = self._environments[name]
        except KeyError:
            msg = 'Update Failed: Environment "{0}" not found.'.format(name)
            _LOG.error(msg)
            # TODO: Add UpdateFailed error
            raise

        _LOG.debug('Update Started: Environment "{0}"'.format(name))

        orig_name = env.name
        orig_parent = env.parent
        orig_description = env.description
        orig_vars = env.variables

        try:
            if new_name:
                msg = 'Updated Environment "{0}": name from "{1}" to "{2}"'.format(env.name, orig_name, new_name)
                env.name = new_name
                _LOG.debug(msg)

            if new_parent:
                msg = 'Updated Environment "{0}": parent from "{1}" to "{2}"'.format(env.name, orig_parent, new_parent)
                env.parent = new_parent
                _LOG.debug(msg)

            if new_description:
                msg = 'Updated Environment "{0}": description'.format(env.name)
                env.description = new_description
                _LOG.debug(msg)

            for var_name, var_value in update_variables.iteritems():
                if var_value is None:
                    msg = 'Updated Environment "{0}": DEL variable "{1}"'.format(env.name, var_name)
                    del env[var_name]
                    _LOG.debug(msg)
                elif var_name in env:
                    msg = 'Updated Environment "{0}": MOD variable "{1}"'.format(env.name, var_name)
                else:
                    msg = 'Updated Environment "{0}": ADD variable "{1"'.format(env.name, var_name)
                env[name] = var_value
                _LOG.debug(msg)
        except Exception as e:
            env.name = orig_name
            env.parent = orig_parent
            env.description = orig_description
            env.update(orig_vars)

            msg = 'Update Failed: Environment "{0}" - {1}'.format(orig_name, e)
            _LOG.error(msg)

            # TODO: Add UpdateFailed error
            raise
        else:
            _LOG.debug('Update Complete: Environment "{0}"'.format(orig_name))

    def delete_environment(self, name):
        self._delete_resource(name, self._environments)

    def find_environments(self, name_pattern=None):
        attr_patterns = [('name', name_pattern)]
        result = self._find_resources(attr_patterns, [self._environments])

        return result

    def create_runtime_profile(self, name, app, environment, cmd_args=None, cmd_kwargs=None, description=None):
        profile = self._create_resource(RuntimeProfile, name, app, environment,
                                        cmd_args=cmd_args, cmd_kwargs=cmd_kwargs, description=description)
        return profile

    def get_runtime_profile(self, name):
        return self._get_resource(name, self._profiles)

    def update_runtime_profile(self, name, new_name=None, new_app=None, new_environment=None,
                               new_cmd_args=None, new_cmd_kwargs=None, new_description=None):
        try:
            profile = self._profiles[name]
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

    def delete_runtime_profile(self, name):
        self._delete_resource(name, self._profiles)

    def find_runtime_profiles(self, name_pattern=None):
        """
        Computes a list of all RuntimeProfile instances whose name matches the name_pattern expression

        Args:
            name_pattern (string): expression used by regex to match against App names.
        """
        attr_patterns = [('name', name_pattern)]
        result = self._find_resources(attr_patterns, [self._profiles])

        return result

    @staticmethod
    def _create_resource(type, collection, name, *args, **kwargs):
        if name in collection:
            msg = 'Creation Failed: {0} "{1}" already exists.'.format(type.__name__, name)
            _LOG.error(msg)
            # TODO: Add ResourceAlreadyExists error
            raise RuntimeError()
        else:
            _LOG.debug('Creation Started: New {0}'.format(type.__name__))

        try:
            resource = type(name, *args, **kwargs)
        except ValueError as e:
            msg = 'Creation Failed: {0}'.format(e)
            _LOG.error(msg)
            # TODO: Add ResourceCreationFailed error
            raise
        else:
            collection[name] = resource

        _LOG.debug('Creation Complete: {0} "{1}"'.format(type.__name__, name))
        return resource

    @staticmethod
    def _get_resource(name, collection):
        try:
            result = collection[name]
        except KeyError:
            _LOG.error('Retrieval Failed: "{0}" not found.'.format(name))
            # TODO: Add ResourceNotFound error
            raise
        else:
            _LOG.debug('Retrieval Complete: "{0}"'.format(name))

        return result

    @staticmethod
    def _delete_resource(name, collection):
        try:
            del collection[name]
        except KeyError:
            msg = 'Delete Failed: "{0}" not found.'
            _LOG.debug(msg)
        else:
            msg = 'Delete Complete: "{0}"'.format(name)
            _LOG.debug(msg)

    @staticmethod
    def _find_resources(attr_patterns, collections):
        # TODO: Memoize
        _LOG.debug('Search Started')

        result = []

        for attribute, pattern in attr_patterns:
            op = operator.attrgetter(attribute)

            if pattern:
                _pattern = unicode(pattern).strip()
            else:
                _LOG.debug('Skipping Attribute "{0}": No Pattern "{1}"'.format(attribute, pattern))
                continue

            if _pattern:
                pattern = re.compile(_pattern)
            else:
                _LOG.debug('Skipping Attribute "{0}": Empty Pattern'.format(attribute))
                continue

            for collection in collections:
                result.extend([resource for resource in collection.itervalues() if pattern.match(op(resource))])

        result.sort(key=operator.attrgetter('name'))

        _LOG.debug('Search Complete: {0:3d} matches'.format(len(result)))
        return result
