import gc
import os

import pytest

import terrarium


class TestEnvironment(object):
    def test_environment_name(self):
        environment = terrarium.Environment('test')
        assert environment.name == 'test'

    def test_environment_settings(self):
        environment = terrarium.Environment('test')
        environment['test_setting'] = 'success'
        assert environment['test_setting'] == 'success'

    def test_environment_set_empty_value(self):
        environment = terrarium.Environment('test')
        with pytest.raises(ValueError):
            environment['EMPTY'] = ''
        with pytest.raises(KeyError):
            value = environment['EMPTY']

    def test_environment_expansion(self):
        environment = terrarium.Environment('test')
        environment['ROOT'] = 'C:'
        environment['FOO'] = '%ROOT%/foo'
        environment['BAR'] = '$FOO/bar'
        environment['BAZ'] = '${BAR}/baz'

        result = environment.expand('%BAZ%/end')
        assert result == os.path.normpath('C:/foo/bar/baz/end')

    def test_environment_compression(self):
        environment = terrarium.Environment('test')
        environment['ROOT'] = 'C:'
        environment['FOO'] = '%ROOT%/foo'
        environment['BAR'] = '$FOO/bar'
        environment['BAZ'] = '${BAR}/baz'

        result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
        assert result == os.path.normpath('$BAZ/end')

    def test_environment_expansion_with_empty_value(self):
        environment = terrarium.Environment('test')
        environment['ROOT'] = 'C:'
        environment['FOO'] = '%ROOT%/foo'
        environment['BAR'] = '$FOO/bar'
        environment['BAZ'] = '${BAR}/baz'

        # Inject empty variable into environment
        environment._vars['EMPTY'] = ''

        result = environment.expand('%BAZ%/end')
        assert result == os.path.normpath('C:/foo/bar/baz/end')

    def test_environment_compression_with_empty_value(self):
        environment = terrarium.Environment('test')
        environment['ROOT'] = 'C:'
        environment['FOO'] = '%ROOT%/foo'
        environment['BAR'] = '$FOO/bar'
        environment['BAZ'] = '${BAR}/baz'

        # Inject empty variable into
        environment._vars['EMPTY'] = ''

        result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
        assert result == os.path.normpath('$BAZ/end')

    def test_environment_tracking(self):
        environment_names = {'Foo', 'Bar', 'Baz'}
        environments = set([terrarium.Environment(en) for en in environment_names])

        assert len(terrarium.Environment.find_environments()) == len(environments)
        assert set([env.name for env in terrarium.Environment.find_environments()]) == environment_names

        environment_names.remove('Bar')
        environments = set([e for e in environments if e.name != 'Bar'])
        gc.collect()

        assert len(terrarium.Environment.find_environments()) == len(environments)
        assert set([env.name for env in terrarium.Environment.find_environments()]) == environment_names


if __name__ == '__main__':
    pytest.main()
