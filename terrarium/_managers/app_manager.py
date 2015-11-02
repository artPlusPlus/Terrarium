import logging

from ..app import App

from ._resource_manager import ResourceManager


_LOG = logging.getLogger(__name__)


class AppManager(ResourceManager):
    def create_app(self, name, location, executable, description=None):
        app = self._create_resource(App, self._resources, name, location, executable, description=description)
        return app

    def get_app(self, name):
        return self._get_resource(name, self._resources)

    def update_app(self, name, new_name=None, new_location=None, new_executable=None, new_description=None):
        try:
            app = self._resources[name]
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
        self._delete_resource(name, self._resources)

    def find_apps(self, name_pattern=None):
        """
        Computes a list of all managed App instances whose name matches the name_pattern expression

        Args:
            name_pattern (string): expression used by regex to match against App names.
        """
        attr_patterns = [('name', name_pattern)]
        result = self._find_resources(attr_patterns, [self._resources])

        return result