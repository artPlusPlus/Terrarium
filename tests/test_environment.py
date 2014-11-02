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
        environment.set_var('test_setting', 'success')
        assert environment.get_setting('test_setting') == 'success'

    def test_environment_set_empty_value(self):
        environment = terrarium.Environment('test')
        with pytest.raises(ValueError):
            environment.set_var('EMPTY', '')
        assert environment.get_setting('EMPTY') is None

    def test_environment_expansion(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        result = environment.expand('%BAZ%/end')
        assert result == os.path.normpath('C:/foo/bar/baz/end')

    def test_environment_compression(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
        assert result == os.path.normpath('$BAZ/end')

    def test_environment_expansion_with_empty_value(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        # Inject empty variable into environment
        environment._vars['EMPTY'] = ''

        result = environment.expand('%BAZ%/end')
        assert result == os.path.normpath('C:/foo/bar/baz/end')

    def test_environment_compression_with_empty_value(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        # Inject empty variable into
        environment._vars['EMPTY'] = ''

        result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
        assert result == os.path.normpath('$BAZ/end')

    def test_environment_tracking(self):
        environment_names = {'Foo', 'Bar', 'Baz'}
        environments = set([terrarium.Environment(en) for en in environment_names])

        assert len(terrarium.Environment.all_environments()) == len(environments)
        assert set([env.name for env in terrarium.Environment.all_environments()]) == environment_names

        environment_names.remove('Bar')
        environments = set([e for e in environments if e.name != 'Bar'])
        gc.collect()

        assert len(terrarium.Environment.all_environments()) == len(environments)
        assert set([env.name for env in terrarium.Environment.all_environments()]) == environment_names


if __name__ == '__main__':
    pytest.main()
