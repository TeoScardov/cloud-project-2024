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
        from accountApp.dbmodel import create_admin_account
        create_admin_account()
        yield app
        db.drop_all() 

@pytest.fixture()
def client(app):
    return app.test_client()