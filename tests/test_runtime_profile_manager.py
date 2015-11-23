import gc
import logging

import pytest

import terrarium

_LOG = logging.getLogger(__name__)


@pytest.fixture
def _profile(request):
    _LOG.debug('create _profile')

    profile = terrarium.RuntimeProfileManager.create_runtime_profile(
        'Test', 'TestApp', 'TestEnv', cmd_args=['foo', 'bar'],
        cmd_kwargs={'baz': 'boz'}, description='This is a test Environment.')

    def fin():
        terrarium.RuntimeProfileManager.delete_runtime_profile(profile.name)
        _LOG.debug('teardown _profile')
    request.addfinalizer(fin)

    return profile


def test_profile_creation(_profile):
    assert _profile
    assert _profile.name == u'Test'
    assert _profile.app == u'TestApp'
    assert _profile.environment == u'TestEnv'
    assert _profile.arguments == [u'foo', u'bar']
    assert _profile.keyword_arguments == {u'baz': u'boz'}


def test_profile_deletion(_profile):
    terrarium.RuntimeProfileManager.delete_runtime_profile('Test')
    gc.collect()

    with pytest.raises(terrarium.ResourceNotFoundError):
        terrarium.RuntimeProfileManager.get_runtime_profile('Test')


def test_profile_retrieval(_profile):
    assert _profile

    retrieved_profile = terrarium.RuntimeProfileManager.get_runtime_profile('Test')

    assert retrieved_profile is _profile


def test_profile_update_name(_profile):
    assert _profile.name == u'Test'

    terrarium.RuntimeProfileManager.update_runtime_profile('Test',
                                                           new_name='Pass')

    assert _profile.name == u'Pass'


def test_profile_update_description(_profile):
    terrarium.RuntimeProfileManager.update_runtime_profile(
        'Test', new_description='This is a Pass Profile!')

    assert _profile.description == u'This is a Pass Profile!'
