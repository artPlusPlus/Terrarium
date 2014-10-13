import nose

import terrarium


class AppTest(object):
    def __init__(self):
        self._app = terrarium.App('Test')

    def test_app_instantiation(self):
        assert self._app
        assert self._app.name == 'Test'


if __name__ == '__main__':
    nose.run()