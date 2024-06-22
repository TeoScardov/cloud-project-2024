import pytest
from flask import jsonify
from unittest.mock import Mock, patch

@pytest.fixture
def dummy_body_purchase():
    return {
        "cart": {
            "total": 20
    }
}
    
@pytest.fixture
def dummy_purchase():
    return {
        "account_id": "123",
        "id": "10",
        "order_date": "2021-01-01",
        "status": "PENDING",
        "total": 20,
    }
    
# Test for health check
def test_health(client):
    response = client.get('/api/purchase/')
    assert response.status_code == 200
    
# Test for creating a new purchase
def test_create_purchase_success(client, dummy_purchase, dummy_body_purchase, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    mock_create = Mock()
    mock_create.return_value = jsonify({'status': 'success', 'message': 'Purchase created', 'purchase': dummy_purchase})

    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.views.createNewPurchase', mock_create)
    response = client.post('/api/purchase/', json=dummy_body_purchase, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json() == {'status': 'success', 'message': 'Purchase created', 'purchase': dummy_purchase}

# Test for creating a new purchase with an invalid token
def test_create_purchase_auth_failure(client, dummy_body_purchase, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/', json=dummy_body_purchase, headers={'Authorization': f'Bearer token'})
    print(response.get_json())
    assert response.status_code == 401
    assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}

# Test for processing a payment
def test_pay_purchase_success(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    mock_pay = Mock()
    mock_pay.return_value = jsonify({'status': 'success', 'message': 'Payment successful'})

    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.views.performPayment', mock_pay)
    response = client.post('/api/purchase/payment', json={'purchase_id': '1', 'amount': 20.0}, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json() == {'status': 'success', 'message': 'Payment successful'}

# Test for processing a payment with an invalid token
def test_pay_purchase_auth_failure(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    
    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/payment', json={'purchase_id': '1', 'amount': 20.0}, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 401
    assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}

# Test for getting a purchase by ID
def test_get_purchase_success(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    mock_get_purchase = Mock()
    mock_get_purchase.return_value = jsonify({
    "purchase": [
        {
            "account_id": "1f91abfa-10e6-4e3b-b3a7-856ddb827031",
            "id": "140b8e81-fbcb-43e5-a864-51e2eeecee23",
            "order_date": "Sat, 22 Jun 2024 18:49:25 GMT",
            "status": "APPROVED",
            "total": 71.28
        }
    ]
})

    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.views.getPurchaseByAccountId', mock_get_purchase)
    response = client.get('/api/purchase/orders', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json() == {
    "purchase": [
        {
            "account_id": "1f91abfa-10e6-4e3b-b3a7-856ddb827031",
            "id": "140b8e81-fbcb-43e5-a864-51e2eeecee23",
            "order_date": "Sat, 22 Jun 2024 18:49:25 GMT",
            "status": "APPROVED",
            "total": 71.28
        }
    ]
}

# Test for getting a purchase by ID with an invalid token
def test_get_purchase_auth_failure(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)

    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.get('/api/purchase/orders', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 401
    assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}