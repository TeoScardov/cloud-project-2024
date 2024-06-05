import pytest
from flask import json

from docker.shopping_cart.app import app as flask_app, drop_test_tables


@pytest.fixture
def app():
    yield flask_app
    # with flask_app.app_context():
    #     drop_test_tables()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session', autouse=True)
def teardown_session(request):
    """
    Teardown function called after all tests in the session have completed.
    """

    def teardown():
        drop_test_tables()  # Call your cleanup function here

    # Register the teardown function to be called after all tests
    request.addfinalizer(teardown)


def test_health(client):
    response = client.get('/api/cart/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'UP'


def test_add_product(client, mocker):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.add_item',
                 return_value=mocker.Mock(id='ace86c09-4113-4155-950a-3560e5da2ee0', total=100))

    response = client.post('/api/cart/addProduct', json={'cart_id': None, 'isbn': '123456'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'product added to cart'
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_remove_product(client, mocker):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value=None)
    mocker.patch('cartApp.database.check_cart_id', return_value=True)
    mocker.patch('cartApp.database.delete_item',
                 return_value=mocker.Mock(id='ace86c09-4113-4155-950a-3560e5da2ee0', total=0, user_id=None,
                                          exp_date=None, items=[]))

    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0', 'isbn': '123456'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'product removed from cart'
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_show_cart(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.check_cart_id', return_value=True)
    mocker.patch('cartApp.database.renew_cart_expiry',
                 return_value=mocker.Mock(id='ace86c09-4113-4155-950a-3560e5da2ee0', total=100))
    mocker.patch('cartApp.database.get_cart_items_by_cart_id', return_value=[{'isbn': '123456', 'quantity': 1}])

    response = client.get('/api/cart/show_cart?cart_id=cart_id')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'
    assert data['total'] == 100
    assert len(data['items']) == 1
    assert data['items'][0]['isbn'] == '123456'


def test_remove_cart(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value=None)
    mocker.patch('cartApp.database.delete_cart', return_value=None)

    response = client.delete('/api/cart/removeCart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'cart deleted successfully'


def test_link_cart(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.link_cart', return_value=None)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.put('/api/cart/link-cart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'},
                          headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'cart linked successfully'


def test_get_cart(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.get_user_cart',
                 return_value=mocker.Mock(id='ace86c09-4113-4155-950a-3560e5da2ee0', user_id='user_id', total=100))
    mocker.patch('cartApp.database.get_cart_items_by_cart_id',
                 return_value=[{'isbn': '123456', 'title': "title", 'price': 20.0}])
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }

    response = client.get('/api/cart/get_cart', headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'
    assert data['total'] == 100
    assert len(data['items']) == 1
    assert data['items'][0]['isbn'] == '123456'
