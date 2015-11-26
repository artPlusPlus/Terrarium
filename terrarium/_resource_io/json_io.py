import logging
import json

from .._resource_managers import AppManager
from .._resource_managers import EnvironmentManager
from .._resource_managers import RuntimeProfileManager
from .._errors import ResourceNotFoundError, ResourceAlreadyExistsError


_LOG = logging.getLogger(__name__)

_FMT_BASE_MISSING_FIELD = 'Failed to load {0} data: No "{{0}}" field found.'
_FMT_BASE_MISSING_FIELD = _FMT_BASE_MISSING_FIELD.format

_FMT_BASE_NULL_DATA = 'Failed to load {0} data: No "{{0}}" field found.'
_FMT_BASE_NULL_DATA = _FMT_BASE_NULL_DATA.format

_FMT_BASE_EMPTY_DATA = 'Failed to load {0} data: No "{{0}}" field found.'
_FMT_BASE_EMPTY_DATA = _FMT_BASE_EMPTY_DATA.format


def import_app(app_data, force=False):
    """
    Creates a managed :class:`terrarium.App` instance from JSON data.

    Args:
        app_data (basestring): JSON string with :class:`terrarium.App` data
        force (bool): If True and an existing app is found, it will be updated

    Returns:
        An :class:`terrarium.App` instance or None
    """
    _LOG.debug('Import Started: App from JSON')

    try:
        app_data = json.loads(app_data)
    except TypeError:
        pass

    fmt_missing_field = _FMT_BASE_MISSING_FIELD('App').format
    fmt_null_data = _FMT_BASE_NULL_DATA('App').format
    fmt_empty_data = _FMT_BASE_EMPTY_DATA('App').format

    def get_data_field(field_name):
        return _get_data_field(app_data, field_name,
                               fmt_missing_field=fmt_missing_field,
                               fmt_null_data=fmt_null_data,
                               fmt_empty_data=fmt_empty_data)

    app_name = get_data_field('name')
    app_location = get_data_field('location')
    app_executable = get_data_field('executable')
    app_description = get_data_field('description')

    try:
        result = AppManager.create_app(app_name, app_location, app_executable,
                                       description=app_description)
    except ResourceAlreadyExistsError:
        if force:
            msg = 'Import Forced: App "{0}" already exists'.format(app_name)
            _LOG.debug(msg)
            AppManager.update_app(app_name, new_location=app_location,
                                  new_executable=app_executable,
                                  new_description=app_description)
            result = AppManager.get_app(app_name)
        else:
            msg = 'Import Failed: App "{0}" already exists'.format(app_name)
            _LOG.error(msg)
            raise ResourceAlreadyExistsError(msg)

    _LOG.debug('Import Complete: App from JSON')
    return result


def export_app(app_name):
    """
    Exports an :class:`terrarium.App` instance to a JSON string.

    Args:
        app_name (basestring): The name of an existing, managed
            :class:`terrarium.App` instance.

    Returns:
        JSON string containing :class:`terrarium.App` data
    """
    _LOG.debug('Export Started: App "{0}" to JSON'.format(app_name))

    try:
        app = AppManager.get_app(app_name)
    except ResourceNotFoundError:
        msg = 'Export Failed: App "{0}" not found.'.format(app_name)
        _LOG.error(msg)
        raise ResourceNotFoundError(msg)

    app_data = {'name': app.name,
                'location': app.location,
                'executable': app.executable,
                'description': app.description}

    _LOG.debug('Export Complete: App "{0}" to JSON'.format(app_name))
    return json.dumps(app_data)


def import_environment(environment_data, force=False):
    """
    Creates a managed :class:`terrarium.Environment` instance from JSON data.

    Args:
        environment_data (basestring): JSON string with
            :class:`terrarium.Environment` data
        force (bool): If True and an existing environment is found,
            it will be updated.

    Returns:
        An :class:`Environment` instance or None
    """
    _LOG.debug('Import Started: Environment from JSON')

    try:
        environment_data = json.loads(environment_data)
    except TypeError:
        pass

    fmt_missing_field = _FMT_BASE_MISSING_FIELD('Environment').format
    fmt_null_data = _FMT_BASE_NULL_DATA('Environment').format
    fmt_empty_data = _FMT_BASE_EMPTY_DATA('Environment').format

    def get_data_field(field_name):
        return _get_data_field(environment_data, field_name,
                               fmt_missing_field=fmt_missing_field,
                               fmt_null_data=fmt_null_data,
                               fmt_empty_data=fmt_empty_data)

    env_name = get_data_field('name')
    env_parent = get_data_field('parent')
    env_variables = get_data_field('variables')
    env_description = get_data_field('description')

    try:
        result = EnvironmentManager.create_environment(
            env_name, parent=env_parent, variables=env_variables,
            description=env_description)
    except ResourceAlreadyExistsError:
        if force:
            msg = 'Import Forced: Environment "{0}" already exists'.format(env_name)
            _LOG.debug(msg)
            EnvironmentManager.update_environment(
                env_name, new_parent=env_parent, update_variables=env_variables,
                new_description=env_description)
            result = EnvironmentManager.get_environment(env_name)
        else:
            msg = 'Import Failed: Environment "{0}" already exists'.format(env_name)
            _LOG.error(msg)
            raise ResourceAlreadyExistsError(msg)

    _LOG.debug('Import Complete: Environment from JSON')
    return result


def export_environment(environment_name):
    """
    Exports an :class:`terrarium.Environment` instance to a JSON string.

    Args:
        environment_name (basestring): The name of an existing, managed
            :class:`terrarium.Environment` instance.

    Returns:
        JSON string containing :class:`terrarium.Environment` data
    """
    _LOG.debug('Export Started: Environment "{0}" to JSON'.format(environment_name))

    try:
        env = EnvironmentManager.get_environment(environment_name)
    except ResourceNotFoundError:
        msg = 'Export Failed: Environment "{0}" not found.'.format(environment_name)
        _LOG.error(msg)
        raise ResourceNotFoundError(msg)

    env_data = {'name': env.name,
                'parent': env.parent,
                'variables': env.variables,
                'description': env.description}

    _LOG.debug('Export Complete: Environment "{0}" to JSON'.format(environment_name))
    return json.dumps(env_data)


def import_runtime_profile(runtime_profile_data, force=False):
    """
    Creates a managed :class:`terrarium.RuntimeProfile` instance from JSON data.

    Args:
        runtime_profile_data (basestring): JSON string with
            :class:`terrarium.RuntimeProfile` data
        force (bool): If True and an existing profile is found, it will be
            updated.

    Returns:
        A :class:`RuntimeProfile` instance or None
    """
    _LOG.debug('Import Started: Runtime Profile from JSON')

    try:
        runtime_profile_data = json.loads(runtime_profile_data)
    except TypeError:
        pass

    fmt_missing_field = _FMT_BASE_MISSING_FIELD('RuntimeProfile').format
    fmt_null_data = _FMT_BASE_NULL_DATA('RuntimeProfile').format
    fmt_empty_data = _FMT_BASE_EMPTY_DATA('RuntimeProfile').format

    def get_data_field(field_name):
        return _get_data_field(runtime_profile_data, field_name,
                               fmt_missing_field=fmt_missing_field,
                               fmt_null_data=fmt_null_data,
                               fmt_empty_data=fmt_empty_data)

    profile_name = get_data_field('name')
    profile_app = get_data_field('app')
    profile_env = get_data_field('environment')
    profile_args = get_data_field('arguments')
    profile_kwargs = get_data_field('keyword_arguments')
    profile_description = get_data_field('description')

    try:
        result = RuntimeProfileManager.create_runtime_profile(
            profile_name, profile_app, profile_env, cmd_args=profile_args,
            cmd_kwargs=profile_kwargs, description=profile_description)
    except ResourceAlreadyExistsError:
        if force:
            msg = 'Import Forced: Runtime Profile "{0}" already exists'.format(profile_name)
            _LOG.debug(msg)
            RuntimeProfileManager.update_runtime_profile(
                profile_name, new_app=profile_app, new_environment=profile_env,
                new_cmd_args=profile_args, new_cmd_kwargs=profile_kwargs,
                new_description=profile_description)
            result = RuntimeProfileManager.get_runtime_profile(profile_name)
        else:
            msg = 'Import Failed: Runtime Profile "{0}" already exists'.format(profile_name)
            _LOG.error(msg)
            raise ResourceAlreadyExistsError(msg)

    _LOG.debug('Import Complete: Runtime Profile from JSON')
    return result


def export_runtime_profile(runtime_profile_name):
    """
    Exports a :class:`terrarium.RuntimeProfile` instance to a JSON string.

    Args:
        runtime_profile_name (basestring): The name of an existing, managed
            :class:`terrarium.RuntimeProfile` instance.

    Returns:
        JSON string containing :class:`terrarium.RuntimeProfile` data
    """
    _LOG.debug('Export Started: Runtime Profile "{0}" to JSON'.format(runtime_profile_name))

    try:
        profile = RuntimeProfileManager.get_runtime_profile(runtime_profile_name)
    except ResourceNotFoundError:
        msg = 'Export Failed: Runtime Profile "{0}" not found.'.format(runtime_profile_name)
        _LOG.error(msg)
        raise ResourceNotFoundError(msg)

    profile_data = {'name': profile.name,
                    'app': profile.app,
                    'environment': profile.environment,
                    'arguments': profile.arguments,
                    'keyword_arguments': profile.keyword_arguments,
                    'description': profile.description}

    _LOG.debug('Export Complete: Runtime Profile "{0}" to JSON'.format(runtime_profile_name))
    return json.dumps(profile_data)


def _get_data_field(data, field_name, fmt_missing_field=None,
                    fmt_null_data=None, fmt_empty_data=None):
    result = None

    try:
        result = data[field_name]
    except KeyError:
        msg = fmt_missing_field(field_name)
        _LOG.error(msg)
        return result

    if result is None:
        msg = fmt_null_data(field_name)
        _LOG.error(msg)
        return result

    if isinstance(result, basestring):
        result = unicode(result).strip()
    if not result:
        msg = fmt_empty_data(field_name)
        _LOG.error(msg)
        return None

    return result
