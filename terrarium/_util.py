import subprocess
import os
import logging

from ._resource_managers import AppManager
from ._resource_managers import EnvironmentManager
from ._resource_managers import RuntimeProfileManager
from ._errors import *

_LOG = logging.getLogger(__name__)

_FMT_CMD_SET = 'SET {0} {1}\n'.format
_FMT_CMD_RUN = 'RUN {0}\n'.format


def apply_environment(environment, overrides=None):
    """
    Pushes the Environment instance's variable data into the current runtime
    environment.

    If a failure occurs while applying a value, any previous value changes will
    be reverted.

    Args:
        environment (string): Name of an existing Environment
        overrides ({str:str}): Mapping of environment variable names and
            values. If a variable name key matches an environment variable
            defined in the Environment instance, the value from the
            override map is used. If an override has no match in the
            Environment instance, it will not be used at all.

    Return:
        None
    """
    if not overrides:
        overrides = {}

    try:
        env = EnvironmentManager.get_environment(environment)
    except KeyError:
        msg = 'Failed to apply environment: Environment "{0}" not found'.format(environment)
        _LOG.error(msg)
        raise ResourceNotFoundError(msg)

    original_env = {}

    for name, value in env.iteritems():
        try:
            value = overrides[name]
        except KeyError:
            pass
        else:
            value = env.expand(value)

        try:
            original_env[name] = os.environ[name]
        except KeyError:
            original_env[name] = None

        try:
            os.environ[name] = value
        except Exception as e:
            msg = 'Failed to apply Environment value "{0}.{1}" - "{2}": {3}'
            msg = msg.format(environment, name, value, e)
            _LOG.error(msg)

            for orig_name, orig_value in original_env.iteritems():
                if orig_value is None:
                    del os.environ[orig_name]
                else:
                    os.environ[orig_name] = orig_value

            raise RuntimeError(msg)


def build_cmd(runtime_profile):
    """
    Computes a command line call string that will run the application.

    Args:
        runtime_profile (string): Name of an existing Runtime Profile

    Returns:
        A string that can be used in a command shell to invoke an application.
    """
    profile = RuntimeProfileManager.get_runtime_profile(runtime_profile)
    app = AppManager.get_app(profile.app)
    env = EnvironmentManager.get_environment(profile.environment)

    result = [os.path.join(env.expand(app.location, app.executable))]
    result.extend([env.expand(arg) for arg in profile.arguments])
    for k, v in profile.keyword_arguments.iteritems():
        if k[0] != '-':
            k = '-{0}'.format(k)
        v = env.expand(v)
        result.append(k)
        result.append(v)
    result = ' '.join(result)

    return result


def execute(runtime_profile):
    """
    Runs an application using the data from the runtime profile.

    Args:
        runtime_profile (string): Name of an existing RuntimeProfile
    """
    profile = RuntimeProfileManager.get_runtime_profile(runtime_profile)
    env = EnvironmentManager.get_environment(profile.environment)

    cmd = build_cmd(runtime_profile)
    subprocess.Popen(cmd, env=env)


def generate_bat(runtime_profile, output_path):
    """
    Creates a batch file that will setup the environment and run an application.

    Args:
        runtime_profile (string): Name of an existing RuntimeProfile
        output_path (string): Absolute file path batch file will be written to.
    """
    profile = RuntimeProfileManager.get_runtime_profile(runtime_profile)
    env = EnvironmentManager.get_environment(profile.environment)

    lines = []

    for name, value in env.iteritems():
        line = _FMT_CMD_SET(name, value)
        lines.append(line)

    line = profile.build_cmd()
    lines.append(line)

    with open(output_path, 'w') as bat:
        bat.writelines(lines)
