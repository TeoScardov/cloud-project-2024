import pytest
from app import create_app
from catalogApp.database import db

@pytest.fixture()
def app():
    app = create_app("testing")
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all() 

@pytest.fixture()
def client(app):
    return app.test_client()