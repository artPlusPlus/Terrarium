import gc

import pytest

import terrarium


class TestApp(object):
    def test_app_instantiation(self):
        app = terrarium.App('Test', '%ROOT%', 'Test.exe')

        assert app
        assert app.name == 'Test'
        assert app.location == '%ROOT%'
        assert app.executable == 'Test.exe'

    def test_app_tracking(self):
        app_foo = terrarium.App('Foo', '%ROOT/Foo/', 'Foo.exe')
        app_bar = terrarium.App('Bar', '%ROOT/Bar/', 'Bar.exe')
        app_baz = terrarium.App('Baz', '%ROOT/Baz/', 'Baz.exe')

        assert len(terrarium.App.all_apps()) == 3
        assert {'Foo', 'Bar', 'Baz'} == set([app.name for app in terrarium.App.all_apps()])

        del app_bar
        gc.collect()
        with pytest.raises(UnboundLocalError):
            assert app_bar is None
        assert len(terrarium.App.all_apps()) == 2
        assert {'Foo', 'Baz'} == set([app.name for app in terrarium.App.all_apps()])

    def test_app_path_resolution(self):
        environment = terrarium.Environment('TestEnv')
        environment.set_var('ROOT', 'C:')
        environment.set_var('APP_DIR', 'Appz/Foo')
        environment.set_var('APP_VERSION', '2015')

        app = terrarium.App('TestApp', '%ROOT%/%APP_DIR%', 'Foo_%APP_VERSION%.exe')

        assert app.resolve_path(environment) == 'C:\\Appz\\Foo\\Foo_2015.exe'

if __name__ == '__main__':
    pytest.main()
