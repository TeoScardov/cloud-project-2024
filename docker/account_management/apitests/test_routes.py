import json
import pytest
#from flask_jwt_extended import create_access_token, decode_token
#from werkzeug.security import generate_password_hash, check_password_hash
from accountApp.database import db
from accountApp.dbmodel import *

def test_health(client):
    response = client.get('/api/account/health')
    assert response.status_code == 200
    assert response.json == {"status": "UP"}
