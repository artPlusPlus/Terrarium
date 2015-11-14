import gc
import logging

import pytest

import terrarium

_LOG = logging.getLogger(__name__)


@pytest.fixture
def _environment(request):
    _LOG.debug('create _environment')

    env = terrarium.EnvironmentManager.create_environment('Test', None,
                                                          description='This is a Test App!')
    def fin():
        terrarium.EnvironmentManager.delete_environment(env.name)
        _LOG.debug('teardown _env')
    request.addfinalizer(fin)

    return env


def test_env_creation(_environment):
    assert _environment
    assert _environment.name == 'Test'
    assert _environment.parent is None
    assert _environment.description == 'This is a Test App!'


def test_env_deletion(_environment):
    terrarium.EnvironmentManager.delete_environment('Test')
    gc.collect()

    with pytest.raises(terrarium.ResourceNotFoundError):
        terrarium.EnvironmentManager.get_environment('Test')


def test_env_retrieval(_environment):
    assert _environment

    retrieved_env = terrarium.EnvironmentManager.get_environment('Test')

    assert retrieved_env is _environment


def test_env_update_name(_environment):
    assert _environment.name == 'Test'

    terrarium.EnvironmentManager.update_environment('Test', new_name='Pass')

    assert _environment.name == 'Pass'


def test_env_update_parent(_environment):
    assert _environment.parent is None

    terrarium.EnvironmentManager.update_environment('Test', new_parent='Pass')

    assert _environment.parent == 'Pass'


def test_env_update_description(_environment):
    terrarium.EnvironmentManager.update_environment('Test', new_description='This is a Pass Env!')

    assert _environment.description == 'This is a Pass Env!'


if __name__ == '__main__':
    pytest.main()
