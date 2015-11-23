import pytest

import terrarium


def test_runtime_profile_instantiation():
    profile = terrarium.RuntimeProfile(
        'TestProfile', 'TestApp', 'TestEnvironment',
        cmd_args=['foo', 'bar'], cmd_kwargs={'baz': 'boz'})

    assert profile
    assert profile.name == u'TestProfile'
    assert profile.app == u'TestApp'
    assert profile.environment == u'TestEnvironment'
    assert profile.arguments == [u'foo', u'bar']
    assert profile.keyword_arguments == {u'baz': u'boz'}


def test_runtime_profile_equivalency():
    profile_a = terrarium.RuntimeProfile(
        'TestProfile', 'TestApp', 'TestEnvironment', cmd_args=['foo', 'bar'],
        cmd_kwargs={'baz': 'boz'})
    profile_b = terrarium.RuntimeProfile(
        'TestProfile', 'TestApp', 'TestEnvironment', cmd_args=['foo', 'bar'],
        cmd_kwargs={'baz': 'boz'})
    profile_c = terrarium.RuntimeProfile(
        'DifferentTestProfile', 'TestApp', 'TestEnvironment',
        cmd_args=['foo', 'bar'], cmd_kwargs={'baz': 'boz'})

    assert profile_a == profile_b
    assert profile_a != profile_c


if __name__ == '__main__':
    pytest.main()
