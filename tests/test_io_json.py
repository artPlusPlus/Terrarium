import logging
import json

import pytest

import terrarium

_LOG = logging.getLogger(__name__)


def test_import_app():
    app_data = {'name': 'TestApp',
                'location': '%ROOT%',
                'executable': 'Test.exe',
                'description': 'I am a test App.'}
    app_data = json.dumps(app_data)
    app = terrarium.json.import_app(app_data)

    assert isinstance(app, terrarium.App)
    assert app == terrarium.AppManager.get_app('TestApp')


def test_import_app_force():
    orig_app = terrarium.AppManager.get_app('TestApp')

    app_data = {'name': 'TestApp',
                'location': '%ROOT%',
                'executable': 'Pass.exe',
                'description': 'I am a test App.'}
    app_data = json.dumps(app_data)

    with pytest.raises(terrarium.ResourceAlreadyExistsError):
        terrarium.json.import_app(app_data)

    updated_app = terrarium.json.import_app(app_data, force=True)

    assert isinstance(updated_app, terrarium.App)
    assert updated_app is orig_app
    assert updated_app is terrarium.AppManager.get_app('TestApp')
    assert updated_app.executable == 'Pass.exe'


def test_export_app():
    app_data = {'name': 'TestApp',
                'location': '%ROOT%',
                'executable': 'Pass.exe',
                'description': 'I am a test App.'}

    exported_data = terrarium.json.export_app('TestApp')
    assert app_data == json.loads(exported_data)


def test_import_environment():
    env_data = {'name': 'TestEnv',
                'parent': None,
                'variables': {'foo': 'bar'},
                'description': 'I am a test Env.'}
    env_data = json.dumps(env_data)
    env = terrarium.json.import_environment(env_data)

    assert isinstance(env, terrarium.Environment)
    assert env == terrarium.EnvironmentManager.get_environment('TestEnv')


def test_import_environment_force():
    orig_env = terrarium.EnvironmentManager.get_environment('TestEnv')

    env_data = {'name': 'TestEnv',
                'parent': 'Pass',
                'variables': {'foo': 'bar'},
                'description': 'I am a test Env.'}
    env_data = json.dumps(env_data)

    with pytest.raises(terrarium.ResourceAlreadyExistsError):
        terrarium.json.import_environment(env_data)

    updated_env = terrarium.json.import_environment(env_data, force=True)

    assert isinstance(updated_env, terrarium.Environment)
    assert updated_env is orig_env
    assert updated_env is terrarium.EnvironmentManager.get_environment('TestEnv')
    assert updated_env.parent == 'Pass'


def test_import_runtime_profile():
    profile_data = {'name': 'TestProfile',
                    'app': 'TestApp',
                    'environment': 'TestEnv',
                    'arguments': ['Foo'],
                    'keyword_arguments': {'Boz': 'Baz'},
                    'description': 'I am a test Runtime Profile.'}
    profile_data = json.dumps(profile_data)
    profile = terrarium.json.import_runtime_profile(profile_data)

    assert isinstance(profile, terrarium.RuntimeProfile)
    assert profile == terrarium.RuntimeProfileManager.get_runtime_profile('TestProfile')


def test_import_runtime_profile_force():
    orig_profile = terrarium.RuntimeProfileManager.get_runtime_profile('TestProfile')

    profile_data = {'name': 'TestProfile',
                    'app': 'PassApp',
                    'environment': 'PassEnv',
                    'arguments': ['Foo'],
                    'keyword_arguments': {'Boz': 'Baz'},
                    'description': 'I am a test Runtime Profile.'}
    profile_data = json.dumps(profile_data)

    with pytest.raises(terrarium.ResourceAlreadyExistsError):
        terrarium.json.import_runtime_profile(profile_data)

    updated_profile = terrarium.json.import_runtime_profile(profile_data, force=True)

    assert isinstance(updated_profile, terrarium.RuntimeProfile)
    assert updated_profile is orig_profile
    assert updated_profile is terrarium.RuntimeProfileManager.get_runtime_profile('TestProfile')
    assert updated_profile.app == 'PassApp'
    assert updated_profile.environment == 'PassEnv'
