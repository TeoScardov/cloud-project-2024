import pytest
from app import create_app
from accountApp.database import db

from app import create_app
@pytest.fixture()
def app():
    app = create_app("testing")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all() 

@pytest.fixture()
def client(app):
    return app.test_client()
