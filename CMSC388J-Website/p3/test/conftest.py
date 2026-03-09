import pytest
import sys, os
from flask_app.app import app as current_app
from flask_app.app import movie_client, mongo


@pytest.fixture
def app(request):
    test_config = {
        "TESTING": True,
        "WTF_CSRF_METHODS": [],
        "WTF_CSRF_ENABLED": False,
    }
    mongo.db.drop_collection('reviews')
    app = current_app
    app.config.update(test_config)

    return app

@pytest.fixture
def client(app):
    return app.test_client()
