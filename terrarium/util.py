import subprocess
import os

from .environment import Environment
from .runtime_profile import RuntimeProfile


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
        env = Environment.find_environments(environment)[0]
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
        app = App.find_apps(self._app)[0]
    except IndexError:
        # TODO: Add Missing app exception
        raise RuntimeError()

    try:
        env = Environment.find_environments(self._environment)[0]
    except IndexError:
        # TODO: Add missing environment exception
        raise RuntimeError()

    result = [os.path.join(env.expand(app.location, app.executable))]
    result.extend([env.expand(arg) for arg in self._args])
    for k, v in self._kwargs.iteritems():
        if k[0] != '-':
            k = '-{0}'.format(k)
        v = env.expand(v)
        result.append(k)
        result.append(v)
    result = ' '.join(result)

    return result


def run(profile):
    """
    Runs an application using the data from the runtime profile.

    Args:
        profile (string): Name of an existing RuntimeProfile
    """
    try:
        profile = RuntimeProfile.find_profiles(profile)[0]
    except IndexError:
        # TODO: Add missing profile exception
        raise RuntimeError()

    try:
        env = Environment.find_environments(profile.environment)[0]
    except IndexError:
        # TODO: Add missing environment exception
        raise RuntimeError()

    cmd = profile.build_cmd()
    subprocess.Popen(cmd, env=env)


def generate_bat(profile, output_path):
    """
    Creates a batch file that will setup the environment and run an application.

    Args:
        profile (string): Name of an existing RuntimeProfile
        output_path (string): Absolute file path batch file will be written to.
    """
    try:
        profile = RuntimeProfile.find_profiles(profile)[0]
    except IndexError:
        # TODO: Add missing profile exception
        raise RuntimeError()

    try:
        env = Environment.find_environments(profile.environment)[0]
    except IndexError:
        # TODO: Add missing environment exception
        raise RuntimeError()

    lines = []

    for name, value in env.iteritems():
        line = _FMT_CMD_SET(name, value)
        lines.append(line)

    line = profile.build_cmd()
    lines.append(line)

    with open(output_path, 'w') as bat:
        bat.writelines(lines)
