import nose

import terrarium


class EnvironmentTest(object):
    def __init__(self):
        self._environment = terrarium.Environment('test')

    def test_environment_instantiation(self):
        assert self._environment
        assert isinstance(self._environment, terrarium.Environment)
        assert self._environment.name == 'test'

    def test_environment_settings(self):
        self._environment.set_setting('test_setting', 'success')
        assert self._environment.get_setting('test_setting') == 'success'

    def test_environment_expansion(self):
        self._environment.set_setting('ROOT', 'C:')
        self._environment.set_setting('FOO', '%ROOT%/foo')
        self._environment.set_setting('BAR', '$FOO/bar')
        self._environment.set_setting('BAZ', '${BAR}/baz')

        result = self._environment.expand('%BAZ%/end')
        assert result == 'C:/foo/bar/baz/end'


if __name__ == '__main__':
    nose.run()