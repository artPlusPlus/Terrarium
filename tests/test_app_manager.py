import gc
import logging

import pytest

import terrarium

_LOG = logging.getLogger(__name__)


@pytest.fixture
def _app(request):
    _LOG.debug('create _app')

    app = terrarium.AppManager.create_app(
        'Test', '%ROOT%', 'Test.exe', description='This is a Test App!')

    def fin():
        terrarium.AppManager.delete_app(app.name)
        _LOG.debug('teardown _app')
    request.addfinalizer(fin)

    return app


def test_app_creation(_app):
    assert _app
    assert _app.name == u'Test'
    assert _app.location == u'%ROOT%'
    assert _app.executable == u'Test.exe'
    assert _app.description == u'This is a Test App!'


def test_app_deletion(_app):
    terrarium.AppManager.delete_app('Test')
    gc.collect()

    with pytest.raises(terrarium.ResourceNotFoundError):
        terrarium.AppManager.get_app('Test')


def test_app_retrieval(_app):
    assert _app

    retrieved_app = terrarium.AppManager.get_app('Test')

    assert retrieved_app is _app


def test_app_update_name(_app):
    assert _app.name == u'Test'

    terrarium.AppManager.update_app('Test', new_name='Pass')

    assert _app.name == u'Pass'


def test_app_update_location(_app):
    assert _app.location == u'%ROOT%'

    terrarium.AppManager.update_app('Test', new_location='%OTHER_ROOT%')

    assert _app.location == u'%OTHER_ROOT%'


def test_app_update_executable(_app):
    assert _app.executable == u'Test.exe'

    terrarium.AppManager.update_app('Test', new_executable='Pass.exe')

    assert _app.executable == u'Pass.exe'


def test_app_update_description(_app):
    terrarium.AppManager.update_app('Test',
                                    new_description='This is a Pass App!')

    assert _app.description == u'This is a Pass App!'


if __name__ == '__main__':
    pytest.main()
