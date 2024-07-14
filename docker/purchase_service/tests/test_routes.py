from unittest import mock
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
def dummy_cart_items():
    return {
        "items" : [
            {"isbn":"db1c8899-05e3-44ac-b2e3-10f3b88ecb04"}, 
            {"isbn":"db1c8899-05e3-44ac-b2e3-10f3b88ecb77"}
            ]
    }
    
@pytest.fixture
def dummy_responce_purchase():
    return {
        "account_id": "123",
        "id": "140b8e81-fbcb-43e5-a864-51e2eeecee23",
        "order_date": "Sat, 22 Jun 2024 18:49:25 GMT",
        "status": "PENDING",
        "total": 20
}
    
@pytest.fixture
def dummy_body_payment():
    return {
        "billing_address":"Cicco",
        "cc": "23423489172639487",
        "expiredate":"22/27",
        "cvv":"444"
}
    
# Test for health check
def test_health(client):
    response = client.get('/api/purchase/')
    assert response.status_code == 200
    
# Test for creating a new purchase
def test_create_purchase_success(client, dummy_body_purchase, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/', json=dummy_body_purchase, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json().keys() == {'status', 'message', 'purchase'}
    assert response.get_json()['purchase'].keys() == {'account_id', 'id', 'order_date', 'status', 'total'}
    assert response.get_json()['purchase']['account_id'] == '123'
    assert response.get_json()['purchase']['total'] == 20
    assert response.get_json()['purchase']['status'] == 'PENDING'
    
# Test for creating a new purchase with missing data
def test_create_purchase_missing_data(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Content type must be application/json'}
    
# Test for creating a new purchase with an empty body
def test_create_purchase_empty_body(client, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/', json={}, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Missing data'}

# Test for creating a new purchase with an invalid token
def test_create_purchase_auth_failure(client, dummy_body_purchase, mocker):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mock_auth = Mock()
    mock_auth.status_code = 401
    mock_auth.get_json.return_value = {'status': 'error', 'message': 'Unauthorized'}
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/', json=dummy_body_purchase, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 401
    assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}
    
# Test for processing a payment
def test_pay_purchase_success(client, mocker, dummy_body_payment, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_body_payment['purchase'] = dummy_responce_purchase
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": dummy_body_payment['purchase']['id']}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch("purchaseApp.controller.requests.post", return_value=mock_responce)
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    response = client.post('/api/purchase/payment', json=dummy_body_payment, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json().keys() == {'status', 'message', 'payment'}
    assert response.get_json()['payment'].keys() == {'id', 'purchase_id'}
    assert response.get_json()['payment']['purchase_id'] == dummy_body_payment['purchase']['id']
    
# Test for processing a payment already processed
def test_pay_purchase_already_processed(client, mocker, dummy_body_payment, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_body_payment['purchase'] = dummy_responce_purchase
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": dummy_body_payment['purchase']['id']}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch("purchaseApp.controller.requests.post", return_value=mock_responce)
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    response = client.post('/api/purchase/payment', json=dummy_body_payment, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400  
    assert response.get_json() == {'status': 'error', 'message': 'Purchase already processed'}
    
# Test for processing a payment already approved
def test_pay_purchase_already_approved(client, mocker, dummy_body_payment, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_body_payment['purchase'] = dummy_responce_purchase
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": dummy_body_payment['purchase']['id']}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch("purchaseApp.controller.requests.post", return_value=mock_responce)
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    response = client.post('/api/purchase/payment', json=dummy_body_payment, headers={'Authorization': f'Bearer token'})
    response = client.post('/api/purchase/payment', json=dummy_body_payment, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400  
    assert response.get_json() == {'status': 'error', 'message': 'Purchase already processed'}
    
# Test for processing a payment that will be rejected
def test_pay_purchase_rejected(client, mocker, dummy_body_payment, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_body_payment['purchase'] = dummy_responce_purchase
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 500
    mock_responce.get_json.return_value ={
            "message": "Payment failed",
            "status": "REJECTED",
            "error": str("Payment failed")
            }
    mock_responce.json.return_value ={
            "message": "Payment failed",
            "status": "REJECTED",
            "error": str("Payment failed")
            }
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch("purchaseApp.controller.requests.post", return_value=mock_responce)
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    response = client.post('/api/purchase/payment', json=dummy_body_payment, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 500  
    assert response.get_json() == {
                'status': 'error',
                'message': 'Payment rejected',
                'error': mock_responce.get_json.return_value
            }
    
# Test for processing a payment that was already rejected
def test_pay_purchase_already_rejected(client, mocker, dummy_body_payment, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'REJECTED'
    dummy_body_payment['purchase'] = dummy_responce_purchase
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value ={"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": dummy_body_payment['purchase']['id']}
    mock_responce.json.return_value ={"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": dummy_body_payment['purchase']['id']}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_payment_dao = Mock(
        id="9a1c8994-1cc5-4305-b29a-621d5a4e7487",
        purchase_id=dummy_body_payment['purchase']['id']
    )
    mock_payment_dao.to_dict.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": dummy_body_payment['purchase']['id']}
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch("purchaseApp.models.PaymentDao.get_by_purchase_id", return_value=mock_payment_dao)
    mocker.patch("purchaseApp.controller.requests.post", return_value=mock_responce)
    response = client.post('/api/purchase/payment', json=dummy_body_payment, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json().keys() == {'status', 'message', 'payment'}

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

# Test for associating books with a purchase
def test_associate_books_success(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": "140b8e81-fbcb-43e5-a864-51e2eeecee23"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/add-book-to-purchase', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    print(response.get_json())
    assert response.status_code == 200
    assert response.get_json() == {'status': 'success', 'message': 'Books associated to purchase'}
    
# Test for associating books with a purchase not approved
def test_associate_books_payment_not_approved(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": "140b8e81-fbcb-43e5-a864-51e2eeecee23"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/add-book-to-purchase', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Purchase not approved'}

# Test for associating books with a purchase with an empty list of books
def test_associate_books_empty_book_list(client, mocker, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": "140b8e81-fbcb-43e5-a864-51e2eeecee23"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": {
            "items": []
        }
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/add-book-to-purchase', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'No books to associate'}
    
# Test for associating books with a purchase with an empty body
def test_associate_books_empty_body(client, mocker, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": "140b8e81-fbcb-43e5-a864-51e2eeecee23"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/add-book-to-purchase', json={}, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Missing data'}

def test_associate_books_missing_data(client, mocker, dummy_responce_purchase):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": "140b8e81-fbcb-43e5-a864-51e2eeecee23"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/add-book-to-purchase', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Content type must be application/json'}

def test_associate_books_already_associated(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"id": "9a1c8994-1cc5-4305-b29a-621d5a4e7487", "purchase_id": "140b8e81-fbcb-43e5-a864-51e2eeecee23"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        isbn=dummy_cart_items['items'][0]['isbn']
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    response = client.post('/api/purchase/add-book-to-purchase', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Purchase already associated with books'}

def test_associate_books_account_success(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_responce.json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        product_id=[item['isbn'] for item in dummy_cart_items['items']]
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.controller.requests.post', return_value=mock_responce)
    response = client.post('/api/purchase/add-book-to-account', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 200
    assert response.get_json() == {"message": "Books associated to account", "status": "success"}
    
def test_associate_books_account_missing_body(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_responce.json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        product_id=[item['isbn'] for item in dummy_cart_items['items']]
    )
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.controller.requests.post', return_value=mock_responce)
    response = client.post('/api/purchase/add-book-to-account', headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Content type must be application/json'}
    
def test_associate_books_account_empty_body(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_responce.json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        product_id=[item['isbn'] for item in dummy_cart_items['items']]
    )
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.controller.requests.post', return_value=mock_responce)
    response = client.post('/api/purchase/add-book-to-account', json={}, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Missing data'}
    
def test_associate_books_account_purchase_not_found(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_responce.json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_purchase_dao = None
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        product_id=[item['isbn'] for item in dummy_cart_items['items']]
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.controller.requests.post', return_value=mock_responce)
    response = client.post('/api/purchase/add-book-to-account', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 404
    assert response.get_json() == {'status': 'error', 'message': 'Purchase not found'}
    
def test_associate_books_account_purchase_unauthorized(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '1234'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_responce.json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        product_id=[item['isbn'] for item in dummy_cart_items['items']]
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.controller.requests.post', return_value=mock_responce)
    response = client.post('/api/purchase/add-book-to-account', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 401
    assert response.get_json() == {'status': 'error', 'message': 'Unauthorized'}
    
def test_associate_books_account_purchase_items_mismatch(client, mocker, dummy_responce_purchase, dummy_cart_items):
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request", lambda *args, **kwargs: None)
    mocker.patch("purchaseApp.controller.SERVICES", {"ACCOUNT_SERVICE" : "http://account_management:5000", "PAYMENT_SERVICE" : "http://payment_service:5000"})
    dummy_responce_purchase['status'] = 'APPROVED'
    mock_auth = Mock()
    mock_auth.status_code = 200
    mock_auth.get_json.return_value = {'account_id': '123'}
    mock_responce = Mock()
    mock_responce.status_code = 200
    mock_responce.get_json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_responce.json.return_value = {"message": "Books associated to account", "status": "success"}
    mock_purchase_dao = Mock(
        account_id=dummy_responce_purchase['account_id'],
        id=dummy_responce_purchase['id'],
        order_date=dummy_responce_purchase['order_date'],
        status=dummy_responce_purchase['status'],
        total=dummy_responce_purchase['total']
    )
    mock_purchase_item_dao = Mock(
        purchase_id=dummy_responce_purchase['id'],
        product_id=dummy_cart_items['items'][0]['isbn']
    )
    dummy_body_add_book = {
        "purchase": dummy_responce_purchase,
        "cart": dummy_cart_items
    }
    mocker.patch("purchaseApp.models.PurchaseDao.get_by_id", return_value=mock_purchase_dao)
    mocker.patch('purchaseApp.views.isAuthenticated', return_value=mock_auth)
    mocker.patch('purchaseApp.models.PurchaseItemDao.get_by_order_id', return_value=mock_purchase_item_dao)
    mocker.patch('purchaseApp.controller.requests.post', return_value=mock_responce)
    response = client.post('/api/purchase/add-book-to-account', json=dummy_body_add_book, headers={'Authorization': f'Bearer token'})
    assert response.status_code == 400
    assert response.get_json() == {'status': 'error', 'message': 'Purchase items mismatch in number of books'}

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
