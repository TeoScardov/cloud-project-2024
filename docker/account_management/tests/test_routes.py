import pytest
from unittest.mock import Mock

@pytest.fixture
def dummy_user_data():
    return {
            'email_address': 'test@example.com',
            'username': 'user',
            'password': 'password',
            'name': 'Test',
            'surname': 'User',
            'role': 'USER'
        }

@pytest.fixture
def admin_credentials():
    from accountApp.config import Config
    return {
            'password': Config.ADMIN_PASSWORD,
            'username': 'admin1',
        }

@pytest.fixture
def dummy_user_credentials():
    from accountApp.config import Config
    return {
            'password': 'password',
            'username': 'user',
        }

@pytest.fixture
def dummy_user_modifications():
    return {
            "username": "user",
            "name": "Test",
            "library": {
                "add": ["ISBN1", "ISBN2", "ISBN3"],
                "delete": ["ISBN4"]
            },
            "phone_number": "0987654321",
            "billing_address": "Roma, Via Roma 1",
            "cc": "1234-5678-9101-1121",
            "expiredate": "12/25",
            "cvv": "123",
            "suspended" : True
        }



def test_health(client):
    response = client.get('/api/account/health')
    assert response.status_code == 200
    assert response.json == {"status": "UP"}



def test_register_missing_json(client):
    response = client.post('/api/account/register', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.json == {"message": "There was a problem with the json file."}

def test_register_username_taken(client, dummy_user_data):
    client.post('/api/account/register', json=dummy_user_data)
    response = client.post('/api/account/register', json=dummy_user_data)
    assert response.status_code == 400
    assert response.json == {"message": "Username already taken."}

def test_register_email_taken(client, dummy_user_data):
    client.post('/api/account/register', json=dummy_user_data)
    dummy_user_data['username'] = 'testuser2'
    response = client.post('/api/account/register', json=dummy_user_data)
    assert response.status_code == 400
    assert response.json == {"message": "E-mail address already in use."}

def test_register_query_error_filter_by(client, mocker, dummy_user_data):
    mock_query = Mock()
    mock_query.filter_by.side_effect = Exception("DB error")  # Simulate an exception on filter_by
    mocker.patch('accountApp.dbmodel.Account.query', new=mock_query)
    response = client.post('/api/account/register', json=dummy_user_data)
    assert response.status_code == 500

def test_register_token_not_valid(client, mocker, dummy_user_data):
    mocker.patch('accountApp.model.authenticate_token', return_value=({"message": "error"}, 400))
    response = client.post('/api/account/register', json=dummy_user_data, headers={'Authorization': f'Bearer invalid_token'})
    assert response.status_code == 400

def test_register_token_not_admin(client, mocker, dummy_user_data):
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "USER"}, 200))
    response = client.post('/api/account/register', json=dummy_user_data, headers={'Authorization': f'Bearer invalid_token'})
    assert response.status_code == 400
    assert response.json == {"message": "The JWT token is not associated to an admin account."}

def test_register_token_error(client, mocker, dummy_user_data):
    mocker.patch('accountApp.model.authenticate_token', side_effect=Exception("Auth error"))
    response = client.post('/api/account/register', json=dummy_user_data, headers={'Authorization': f'Bearer invalid_token'})
    assert response.status_code == 400
    assert response.json == {"message": "There was an error related to the authorization token."}

def test_register_parsing_error(client):
    data = {'username': 'baduser', "email_address": "test@example.com"}     # Missing fields
    response = client.post('/api/account/register', json=data)
    assert response.status_code == 400
    assert response.json == {"message": "There was an error while parsing the data."}

def test_register_db_error_add_account(client, mocker, dummy_user_data):
    mocker.patch('accountApp.database.db.session.add', side_effect=Exception("Auth error"))
    response = client.post('/api/account/register', json=dummy_user_data)
    assert response.status_code == 500
    assert response.json == {"message": "There was an error in the database registration process for the account."}

def test_register_db_error_add_customer(client, mocker, dummy_user_data):
    mocker.patch('accountApp.database.db.session.add', side_effect=[None, Exception("Auth error")])
    response = client.post('/api/account/register', json=dummy_user_data)
    assert response.status_code == 500
    assert response.json == {"message": "There was an error in the database registration process for the customer."}

def test_register_success_user(client, dummy_user_data):
    response = client.post('/api/account/register', json=dummy_user_data)
    assert response.status_code == 200
    assert response.json == {"message": "The registration was succesful."}

def test_register_success_admin(client, mocker, dummy_user_data):
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN"}, 200))
    response = client.post('/api/account/register', json=dummy_user_data, headers={'Authorization': f'Bearer valid_token'})
    assert response.status_code == 200
    assert response.json == {"message": "The registration was succesful."}



def test_login_missing_json(client):
    response = client.post('/api/account/login', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.json == {"message": "There was a problem with the json file."}

def test_login_database_error(client, mocker, dummy_user_data):
    mock_query = Mock()
    mock_query.filter_by.side_effect = Exception("DB error")
    mocker.patch('accountApp.dbmodel.Account.query', new=mock_query)
    response = client.post('/api/account/login', json=dummy_user_data)
    assert response.status_code == 500
    assert response.json == {"message": "There was a problem with the database querying."}

def test_login_nonexisting_account(client, dummy_user_data):
    response = client.post('/api/account/login', json=dummy_user_data)
    assert response.status_code == 400
    assert response.json == {"message": "Account not found."}

def test_login_suspended(client, mocker, dummy_user_data):
    mock_query = Mock()
    mock_query.filter_by.return_value.suspended = True
    mocker.patch('accountApp.dbmodel.Account.query', new=mock_query)
    response = client.post('/api/account/login', json=dummy_user_data)
    assert response.status_code == 400
    assert response.json == {"message": "The account was suspended."}

def test_login_success(client, mocker, dummy_user_data):
    mocker.patch('accountApp.model.create_access_token', return_value="token")
    client.post('/api/account/register', json=dummy_user_data)
    response = client.post('/api/account/login', json=dummy_user_data)
    assert response.status_code == 200
    assert response.json["message"] == "Login successful."

def test_login_wrong_password(client, mocker, dummy_user_data):
    mocker.patch('accountApp.model.create_access_token', return_value="token")
    client.post('/api/account/register', json=dummy_user_data)
    dummy_user_data["password"] = "wrong_password"
    response = client.post('/api/account/login', json=dummy_user_data)
    assert response.status_code == 400
    assert response.json == {"message": "The password is not correct."}



def test_logout(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    response = client.post('/api/account/logout')
    assert response.status_code == 200
    assert response.json == {"message": "Logged out."}



def test_update_missing_json(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    response = client.post('/api/account/update', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.json == {"message": "There was a problem with the json file."}

def test_update_requestor_authentication_error(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({}, 400))
    response = client.post('/api/account/update', json={}, headers={'Authorization': f'Bearer invalid_token'})
    assert response.status_code == 400

def test_update_missing_id_to_modify(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin"}, 200))
    response = client.post('/api/account/update', json={}, headers={'Authorization': f'Bearer admin_token'})
    assert response.status_code == 400
    assert response.json == {"message": 'Must specify an "account_id" or "username".'}

def test_update_username_to_modify_not_found(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin"}, 200))
    response = client.post('/api/account/update', json={'username': 'nonexistant_user'}, headers={'Authorization': f'Bearer admin_token'})
    assert response.status_code == 400
    assert response.json == {"message": "Username not valid."}

def test_update_id_to_modify_not_found(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin"}, 200))
    response = client.post('/api/account/update', json={'account_id': 'nonexistant_id'}, headers={'Authorization': f'Bearer admin_token'})
    assert response.status_code == 400
    assert response.json == {"message": "Account id not valid."}

def test_update_db_query_error(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin"}, 200))
    mock_query = Mock()
    mock_query.filter_by.side_effect = Exception("DB error")
    mocker.patch('accountApp.dbmodel.Account.query', new=mock_query)
    response = client.post('/api/account/update', json={'username': 'user'}, headers={'Authorization': f'Bearer admin_token'})
    assert response.status_code == 500
    assert response.json == {"message": "There was a problem with the database querying."}

def test_update_success_user(client, mocker, dummy_user_data, dummy_user_modifications):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=dummy_user_data)
    user_id = login.json['access_token']
    dummy_user_modifications['account_id'] = user_id
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "USER", "account_id": user_id}, 200))
    response = client.post('/api/account/update', json=dummy_user_modifications, headers={'Authorization': f'Bearer {user_id}'})
    assert response.status_code == 200
    assert response.json == {"message": "Info successfully updated."}

def test_update_success_admin(client, mocker, dummy_user_data, admin_credentials, dummy_user_modifications):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=admin_credentials)
    admin_token = login.json['access_token']
    login = client.post('/api/account/login', json=dummy_user_data)
    user_id = login.json['access_token']
    dummy_user_modifications['account_id'] = user_id
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": admin_token}, 200))
    response = client.post('/api/account/update', json=dummy_user_modifications, headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert response.json == {"message": "Info successfully updated."}

def test_update_db_commit_error(client, mocker, dummy_user_data, dummy_user_modifications):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=dummy_user_data)
    user_id = login.json['access_token']
    dummy_user_modifications['account_id'] = user_id
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "USER", "account_id": user_id}, 200))
    mocker.patch('accountApp.database.db.session.commit', side_effect=Exception("Auth error"))
    response = client.post('/api/account/update', json=dummy_user_modifications, headers={'Authorization': f'Bearer {user_id}'})
    assert response.status_code == 500
    assert response.json == {"message": "The info could not be updated."}



def test_authenticate_invalid_token(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    response = client.post('/api/account/authenticate', headers={'Authorization': f'bad_string'})
    assert response.status_code == 400
    assert response.json == {"message": "Token not valid"}

def test_authenticate_account_not_found(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("accountApp.model.decode_token", lambda *args, **kwargs: {'sub': args[0]})
    response = client.post('/api/account/authenticate', headers={'Authorization': f'Bearer invalid_token'})
    assert response.status_code == 400
    assert response.json == {"message": "Account not found."}

def test_authenticate_success_user(client, mocker, dummy_user_data):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=dummy_user_data)
    user_token = login.json['access_token']
    mocker.patch("accountApp.model.decode_token", lambda *args, **kwargs: {'sub': args[0]})
    response = client.post('/api/account/authenticate', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    assert response.json["message"] == "Account successfully authenticated"

def test_authenticate_success_admin(client, mocker, admin_credentials):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=admin_credentials)
    admin_token = login.json['access_token']
    mocker.patch("accountApp.model.decode_token", lambda *args, **kwargs: {'sub': args[0]})
    response = client.post('/api/account/authenticate', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    assert response.json["message"] == "Account successfully authenticated"

def test_authenticate_db_query_error(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("accountApp.model.decode_token", lambda *args, **kwargs: {'sub': args[0]})
    mock_query = Mock()
    mock_query.filter_by.side_effect = Exception("DB error") 
    mocker.patch('accountApp.dbmodel.Account.query', new=mock_query)
    response = client.post('/api/account/authenticate', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 500
    assert response.json == {"message": "There was a problem with the database querying."}



def test_info_invalid_token(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({}, 400))
    response = client.post('/api/account/info', json={}, headers={'Authorization': f'Bearer invalid_token'})
    assert response.status_code == 400

def test_info_missing_json_in_admin_request(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin_id"}, 200))
    response = client.post('/api/account/info', json={}, headers={'Authorization': f'Bearer valid_token'})
    assert response.status_code == 400
    assert response.json == {"message": 'Must specify an "account_id" or "username".'}
 
def test_info_username_not_valid(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin_id"}, 200))
    response = client.post('/api/account/info', json={'username': 'invalid'}, headers={'Authorization': f'Bearer valid_token'})
    assert response.status_code == 400
    assert response.json == {"message": "Username not valid."}

def test_info_account_id_not_valid(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin_id"}, 200))
    response = client.post('/api/account/info', json={'account_id': 'invalid'}, headers={'Authorization': f'Bearer valid_token'})
    assert response.status_code == 400
    assert response.json == {"message": "Account id not valid."}

def test_info_db_query_error(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": "admin_id"}, 200))
    mock_query = Mock()
    mock_query.filter_by.side_effect = Exception("DB error")  
    mocker.patch('accountApp.dbmodel.Account.query', new=mock_query)
    response = client.post('/api/account/info', json={'account_id': 'test_id'}, headers={'Authorization': f'Bearer valid_token'})
    assert response.status_code == 500
    assert response.json == {"message": "There was a problem with the database querying."}

def test_info_success_user(client, mocker, dummy_user_data, dummy_user_modifications):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=dummy_user_data)
    user_id = login.json['access_token']
    dummy_user_modifications['account_id'] = user_id
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "USER", "account_id": user_id}, 200))
    response = client.post('/api/account/info', json=dummy_user_modifications, headers={'Authorization': f'Bearer {user_id}'})
    assert response.status_code == 200

def test_info_success_user_with_modifications(client, mocker, dummy_user_data, dummy_user_modifications):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=dummy_user_data)
    user_id = login.json['access_token']
    dummy_user_modifications['account_id'] = user_id
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "USER", "account_id": user_id}, 200))
    response1 = client.post('/api/account/info', headers={'Authorization': f'Bearer {user_id}'})
    client.post('/api/account/update', json=dummy_user_modifications, headers={'Authorization': f'Bearer {user_id}'})
    response2 = client.post('/api/account/info', headers={'Authorization': f'Bearer {user_id}'})
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response2.json["phone_number"] == dummy_user_modifications["phone_number"]

def test_info_success_admin_specify_user(client, mocker, dummy_user_data, admin_credentials):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    client.post('/api/account/register', json=dummy_user_data)
    mocker.patch("accountApp.model.create_access_token", lambda *args, **kwargs: kwargs['identity'])
    login = client.post('/api/account/login', json=admin_credentials)
    access_token = login.json['access_token']
    mocker.patch('accountApp.model.authenticate_token', return_value=({"role": "ADMIN", "account_id": access_token}, 200))
    response = client.post('/api/account/info', json={'username': 'user'}, headers={'Authorization': f'Bearer {access_token}'})
    assert response.status_code == 200
