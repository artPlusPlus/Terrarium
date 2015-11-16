import os

import pytest

import terrarium


def test_environment_name():
    environment = terrarium.Environment('test')
    assert environment.name == 'test'


def test_environment_settings():
    environment = terrarium.Environment('test')
    environment['test_setting'] = 'success'
    assert environment['test_setting'] == 'success'


def test_environment_set_empty_value():
    environment = terrarium.Environment('test')
    with pytest.raises(ValueError):
        environment['EMPTY'] = ''
    with pytest.raises(KeyError):
        value = environment['EMPTY']


def test_environment_expansion():
    environment = terrarium.Environment('test')
    environment['ROOT'] = 'C:'
    environment['FOO'] = '%ROOT%/foo'
    environment['BAR'] = '$FOO/bar'
    environment['BAZ'] = '${BAR}/baz'

    result = environment.expand('%BAZ%/end')
    assert result == os.path.normpath('C:/foo/bar/baz/end')


def test_environment_compression():
    environment = terrarium.Environment('test')
    environment['ROOT'] = 'C:'
    environment['FOO'] = '%ROOT%/foo'
    environment['BAR'] = '$FOO/bar'
    environment['BAZ'] = '${BAR}/baz'

    result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
    assert result == os.path.normpath('$BAZ/end')


def test_environment_expansion_with_empty_value():
    environment = terrarium.Environment('test')
    environment['ROOT'] = 'C:'
    environment['FOO'] = '%ROOT%/foo'
    environment['BAR'] = '$FOO/bar'
    environment['BAZ'] = '${BAR}/baz'

    # Inject empty variable into environment
    environment._vars['EMPTY'] = ''

    result = environment.expand('%BAZ%/end')
    assert result == os.path.normpath('C:/foo/bar/baz/end')


def test_environment_compression_with_empty_value():
    environment = terrarium.Environment('test')
    environment['ROOT'] = 'C:'
    environment['FOO'] = '%ROOT%/foo'
    environment['BAR'] = '$FOO/bar'
    environment['BAZ'] = '${BAR}/baz'

    # Inject empty variable into
    environment._vars['EMPTY'] = ''

    result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
    assert result == os.path.normpath('$BAZ/end')


if __name__ == '__main__':
    pytest.main()
