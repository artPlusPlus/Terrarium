import pytest

import terrarium


def test_runtime_profile_instantiation():
    profile = terrarium.RuntimeProfile('TestProfile', 'TestApp', 'TestEnvironment',
                                       cmd_args=['foo', 'bar'], cmd_kwargs={'baz': 'boz'})

    assert profile
    assert profile.name == 'TestProfile'
    assert profile.app == 'TestApp'
    assert profile.environment == 'TestEnvironment'
    assert profile.arguments == ['foo', 'bar']
    assert profile.keyword_arguments == {'baz': 'boz'}


def test_runtime_profile_equivalency():
    profile_a = terrarium.RuntimeProfile('TestProfile', 'TestApp', 'TestEnvironment',
                                         cmd_args=['foo', 'bar'], cmd_kwargs={'baz': 'boz'})
    profile_b = terrarium.RuntimeProfile('TestProfile', 'TestApp', 'TestEnvironment',
                                         cmd_args=['foo', 'bar'], cmd_kwargs={'baz': 'boz'})
    profile_c = terrarium.RuntimeProfile('DifferentTestProfile', 'TestApp', 'TestEnvironment',
                                         cmd_args=['foo', 'bar'], cmd_kwargs={'baz': 'boz'})

    assert profile_a == profile_b
    assert profile_a != profile_c


if __name__ == '__main__':
    pytest.main()
