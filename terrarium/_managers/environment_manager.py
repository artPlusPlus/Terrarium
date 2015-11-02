import logging

from ..environment import Environment

from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class EnvironmentManager(ResourceManager):
    def create_environment(self, name, parent, description=None):
        env = self._create_resource(Environment, self._resources, name, parent, description=description)
        return env

    def get_environment(self, name):
        return self._get_resource(name, self._resources)

    def update_environment(self, name, new_name=None, new_parent=None, new_description=None, update_variables=None):
        try:
            env = self._resources[name]
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
        self._delete_resource(name, self._resources)

    def find_environments(self, name_pattern=None):
        attr_patterns = [('name', name_pattern)]
        result = self._find_resources(attr_patterns, [self._resources])

        return result
