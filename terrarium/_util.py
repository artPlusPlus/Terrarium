import subprocess
import os

from ._resource_managers import AppManager
from ._resource_managers import EnvironmentManager
from ._resource_managers import RuntimeProfileManager


_FMT_CMD_SET = 'SET {0} {1}\n'.format
_FMT_CMD_RUN = 'RUN {0}\n'.format


def apply_environment(environment, overrides=None):
    """
    Pushes the Environment instance's variable data into the current
        runtime environment

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
    except IndexError:
        # TODO: Adding missing environment exception
        raise RuntimeError()

    for name, value in env.iteritems():
        try:
            value = overrides[name]
        except KeyError:
            pass
        else:
            value = env.expand(value)

        os.environ[name] = value


def build_cmd(runtime_profile):
    """
    Computes a command line call string that will run the application.

    Args:
        runtime_profile (string): Name of an existing Runtime Profile

    Returns:
        A string that can be used in a command shell to invoke an application.
    """
    try:
        profile = RuntimeProfileManager.get_runtime_profile(runtime_profile)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

    try:
        app = AppManager.get_app(profile.app)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

    try:
        env = EnvironmentManager.get_environment(profile.environment)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

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
    try:
        profile = RuntimeProfileManager.get_runtime_profile(runtime_profile)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

    try:
        env = EnvironmentManager.get_environment(profile.environment)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

    cmd = build_cmd(runtime_profile)
    subprocess.Popen(cmd, env=env)


def generate_bat(runtime_profile, output_path):
    """
    Creates a batch file that will setup the environment and run an application.

    Args:
        runtime_profile (string): Name of an existing RuntimeProfile
        output_path (string): Absolute file path batch file will be written to.
    """
    try:
        profile = RuntimeProfileManager.get_runtime_profile(runtime_profile)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

    try:
        env = EnvironmentManager.get_environment(profile.environment)
    except KeyError as e:  # TODO: Implement ResourceNotFound Handler
        raise RuntimeError()

    lines = []

    for name, value in env.iteritems():
        line = _FMT_CMD_SET(name, value)
        lines.append(line)

    line = profile.build_cmd()
    lines.append(line)

    with open(output_path, 'w') as bat:
        bat.writelines(lines)
