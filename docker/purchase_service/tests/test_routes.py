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
    

    

def test_health(client):
    response = client.get('/api/purchase/')
    assert response.status_code == 200
    
# Test for creating a new purchase
def test_create_purchase_success(client, dummy_purchase, dummy_body_purchase):
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    #mock_create = Mock()
    #mock_create.return_value = jsonify({'status': 'success', 'message': 'Purchase created', 'purchase': dummy_purchase})

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        #with patch('purchaseApp.views.createNewPurchase', mock_create):
            response = client.post('/api/purchase/', json=dummy_body_purchase, headers={'Authorization': f'Bearer token'})
            print(response.get_json())
            assert response.status_code == 200
            assert response.get_json() == {'status': 'success', 'message': 'Purchase created', 'purchase': dummy_purchase}

def test_create_purchase_auth_failure(client):
    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        response = client.post('/api/purchase', json={'item': 'book', 'price': 20.0}, headers={'Authorization': 'Bearer testtoken'})
        assert response.status_code == 401
        assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}

# Test for processing a payment
def test_pay_purchase_success(client):
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    mock_pay = Mock()
    mock_pay.return_value = jsonify({'status': 'success', 'message': 'Payment successful'})

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        with patch('purchaseApp.views.performPayment', mock_pay):
            response = client.post('/api/purchase/payment', json={'purchase_id': '1', 'amount': 20.0}, headers={'Authorization': 'Bearer testtoken'})
            assert response.status_code == 200
            assert response.get_json() == {'status': 'success', 'message': 'Payment successful'}

def test_pay_purchase_auth_failure(client):
    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        response = client.post('/api/purchase/payment', json={'purchase_id': '1', 'amount': 20.0}, headers={'Authorization': 'Bearer testtoken'})
        assert response.status_code == 401
        assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}

# Test for getting a purchase by ID
def test_get_purchase_by_id_success(client):
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    mock_get_purchase = Mock()
    mock_get_purchase.return_value = jsonify({'id': '1', 'item': 'book', 'price': 20.0})

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        with patch('purchaseApp.views.getPurchaseById', mock_get_purchase):
            response = client.get('/api/purchase/purchase/1', headers={'Authorization': 'Bearer testtoken'})
            assert response.status_code == 200
            assert response.get_json() == {'id': '1', 'item': 'book', 'price': 20.0}

def test_get_purchase_by_id_auth_failure(client):
    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        response = client.get('/api/purchase/purchase/1', headers={'Authorization': 'Bearer testtoken'})
        assert response.status_code == 401
        assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}

# Test for getting all purchases for an account
def test_get_purchases_success(client):
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}

    mock_get_purchases = Mock()
    mock_get_purchases.return_value = jsonify([{'id': '1', 'item': 'book', 'price': 20.0}, {'id': '2', 'item': 'pen', 'price': 5.0}])

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        with patch('purchaseApp.views.getPurchasesByAccountId', mock_get_purchases):
            response = client.get('/api/purchase/purchases', headers={'Authorization': 'Bearer testtoken'})
            assert response.status_code == 200
            assert response.get_json() == [{'id': '1', 'item': 'book', 'price': 20.0}, {'id': '2', 'item': 'pen', 'price': 5.0}]

def test_get_purchases_auth_failure(client):
    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}

    with patch('purchaseApp.views.isAuthenticated', return_value=mock_auth):
        response = client.get('/api/purchase/purchases', headers={'Authorization': 'Bearer testtoken'})
        assert response.status_code == 401
        assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}