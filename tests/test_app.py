import pytest

import terrarium


def test_app_instantiation():
    app = terrarium.App('Test', '%ROOT%', 'Test.exe')

    assert app
    assert app.name == 'Test'
    assert app.location == '%ROOT%'
    assert app.executable == 'Test.exe'


def test_app_equivalency():
    app_a = terrarium.App('Test', '%ROOT%', 'Test.exe')
    app_b = terrarium.App('Test', '%ROOT%', 'Test.exe')

    assert app_a == app_b


if __name__ == '__main__':
    pytest.main()
