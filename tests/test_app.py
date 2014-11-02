import gc
import os

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
        app_names = {'Foo', 'Bar', 'Baz'}
        apps = set([terrarium.App(n, '%ROOT/{}'.format(n), '{}.exe') for n in app_names])

        assert len(terrarium.App.all_apps()) == len(apps)
        assert set([app.name for app in terrarium.App.all_apps()]) == app_names

        app_names = {'Foo', 'Baz'}
        apps = set([app for app in apps if app.name != 'Bar'])
        gc.collect()

        assert len(terrarium.App.all_apps()) == len(apps)
        assert set([app.name for app in terrarium.App.all_apps()]) == app_names

    def test_app_path_resolution(self):
        environment = terrarium.Environment('TestEnv')
        environment.set_var('ROOT', 'C:')
        environment.set_var('APP_DIR', 'Appz/Foo')
        environment.set_var('APP_VERSION', '2015')

        app = terrarium.App('TestApp', '%ROOT%/%APP_DIR%', 'Foo_%APP_VERSION%.exe')

        assert app.resolve_path(environment) == os.path.normpath('C:/Appz/Foo/Foo_2015.exe')

if __name__ == '__main__':
    pytest.main()
