import gc
import time

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
        assert result == 'C:\\foo\\bar\\baz\\end'

    def test_environment_compression(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
        assert result == '$BAZ\\end'

    def test_environment_expansion_with_empty_value(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        # Inject empty variable into environment
        environment._vars['EMPTY'] = ''

        result = environment.expand('%BAZ%/end')
        assert result == 'C:\\foo\\bar\\baz\\end'

    def test_environment_compression_with_empty_value(self):
        environment = terrarium.Environment('test')
        environment.set_var('ROOT', 'C:')
        environment.set_var('FOO', '%ROOT%/foo')
        environment.set_var('BAR', '$FOO/bar')
        environment.set_var('BAZ', '${BAR}/baz')

        # Inject empty variable into
        environment._vars['EMPTY'] = ''

        result = environment.compress('C:/foo/bar/baz/end', var_format='${0}')
        assert result == '$BAZ\\end'

    def test_environment_tracking(self):
        env_foo = terrarium.Environment('Foo')
        env_bar = terrarium.Environment('Bar')
        env_baz = terrarium.Environment('Baz')

        assert len(terrarium.Environment.all_environments()) == 3
        assert {'Foo', 'Bar', 'Baz'} == set([env.name for env in terrarium.Environment.all_environments()])

        env_bar = None
        del env_bar
        gc.collect()

        with pytest.raises(UnboundLocalError):
            assert env_bar is None

        assert len(terrarium.Environment.all_environments()) == 2
        assert {'Foo', 'Baz'} == set([env.name for env in terrarium.Environment.all_environments()])


if __name__ == '__main__':
    pytest.main()
