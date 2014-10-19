import nose

import terrarium


class TestEnvironment(object):
    def __init__(self):
        self._environment = terrarium.Environment('test')

    def test_environment_instantiation(self):
        assert self._environment
        assert isinstance(self._environment, terrarium.Environment)
        assert self._environment.name == 'test'

    def test_environment_settings(self):
        self._environment.set_var('test_setting', 'success')
        assert self._environment.get_setting('test_setting') == 'success'

    def test_environment_expansion(self):
        self._environment.set_var('ROOT', 'C:')
        self._environment.set_var('FOO', '%ROOT%/foo')
        self._environment.set_var('BAR', '$FOO/bar')
        self._environment.set_var('BAZ', '${BAR}/baz')

        result = self._environment.expand('%BAZ%/end', use_runtime_environment=False)
        assert result == 'C:/foo/bar/baz/end'

    def test_environment_compression(self):
        self._environment.set_var('ROOT', 'C:')
        self._environment.set_var('FOO', '%ROOT%/foo')
        self._environment.set_var('BAR', '$FOO/bar')
        self._environment.set_var('BAZ', '${BAR}/baz')

        result = self._environment.compress('C:/foo/bar/baz/end', var_format='${0}', use_runtime_environment=True)
        assert result == '$BAZ/end'

if __name__ == '__main__':
    nose.run()
