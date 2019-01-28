import pytest
from api import create_app

@pytest.fixture
def app():
    app = create_app('test_config.py')
    app.debug = True
    return app