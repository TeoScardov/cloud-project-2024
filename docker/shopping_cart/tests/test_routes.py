import pytest
from flask import json

CART = {
    'id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
    'total': 60.0,
    'user_id': None,
    'exp_date': 'exp_date',
    'items': [
        {
            'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
            'isbn': '978-0-306-40615-1',
            'title': 'abcd',
            'price': 10.0,
        },
        {
            'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
            'isbn': '978-0-306-40615-2',
            'title': 'bcde',
            'price': 20.0,
        },
        {
            'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
            'isbn': '978-0-306-40615-3',
            'title': 'cdef',
            'price': 30.0,
        }
    ]
}


# @pytest.fixture
# def app():
#     yield flask_app


# @pytest.fixture
# def client(app):
#     return app.test_client()


@pytest.fixture
def sample_cart(mocker):
    return mocker.Mock(id='ace86c09-4113-4155-950a-3560e5da2ee0',
                       total=60.0,
                       user_id=None,
                       exp_date='2020-01-01',
                       items=[
                           {
                               'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
                               'isbn': '978-0-306-40615-1',
                               'title': 'abcd',
                               'price': 10.0,
                           },
                           {
                               'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
                               'isbn': '978-0-306-40615-2',
                               'title': 'bcde',
                               'price': 20.0,
                           },
                           {
                               'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0',
                               'isbn': '978-0-306-40615-3',
                               'title': 'cdef',
                               'price': 30.0,
                           }
                       ])


# @pytest.fixture(scope='session', autouse=True)
# def teardown_session(request, drop_test_tables):
#     """
#     Teardown function called after all tests in the session have completed.
#     """

#     def teardown():
#         drop_test_tables()  # Call your cleanup function here

#     # Register the teardown function to be called after all tests
#     request.addfinalizer(teardown)

def test_health(client):
    response = client.get('/api/cart/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'UP'


def test_add_product_success(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value=None)
    mocker.patch('cartApp.database.add_item',
                 return_value=sample_cart)

    response = client.post('/api/cart/addProduct', json={'cart_id': None, 'isbn': '123456'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'product added to cart'
    #assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_add_product_existing_cart_success_(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value=None)
    mocker.patch('cartApp.database.check_cart_id', return_value=sample_cart)
    mocker.patch('cartApp.database.renew_cart_expiry', return_value=sample_cart)
    mocker.patch('cartApp.database.add_item',
                 return_value=sample_cart)

    response = client.post('/api/cart/addProduct',
                           json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0', 'isbn': '123456'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'product added to cart'
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_add_product_no_cart_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_cart_id', return_value=None)
    mocker.patch('cartApp.database.add_item',
                 return_value=sample_cart)

    response = client.post('/api/cart/addProduct',
                           json={'cart_id': "ace86c09-4113-4155-950a-3560e5da4er0", 'isbn': '123456'})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Invalid/Not existing cart ID'


def test_add_product_item_already_exists_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.check_cart_id', return_value=sample_cart)
    mocker.patch('cartApp.database.renew_cart_expiry', return_value=sample_cart)
    mocker.patch('cartApp.database.add_item',
                 side_effect=Exception('Item already exists in cart, you cannot add each item more than once'))

    response = client.post('/api/cart/addProduct',
                           json={'cart_id': "ace86c09-4113-4155-950a-3560e5da4er0", 'isbn': '123456'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'Item already exists in cart, you cannot add each item more than once'


def test_add_product_item_already_exists_new_cart_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.insert_cart', return_value='ace86c09-4113-4155-950a-3560e5da4er0')
    mocker.patch('cartApp.database.add_item',
                 side_effect=Exception('Item already exists in cart, you cannot add each item more than once'))

    response = client.post('/api/cart/addProduct', json={'cart_id': None, 'isbn': '123456'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'Item already exists in cart, you cannot add each item more than once'


def test_add_product_cart_id_mismatch_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    mocker.patch('cartApp.database.check_cart_id', return_value=None)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }

    response = client.post('/api/cart/addProduct',
                           json={'cart_id': "edr46c09-4113-4155-950a-3560e5da4er0", 'isbn': '123456'}, headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID mismatch'
    assert data['cart_id'] == 'edr46c09-4113-4155-950a-3560e5da4er0'
    assert data['user_cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_add_product_invalid_jwt_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', side_effect=Exception)
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    mocker.patch('cartApp.database.check_cart_id', return_value=None)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }

    response = client.post('/api/cart/addProduct',
                           json={'cart_id': "edr46c09-4113-4155-950a-3560e5da4er0", 'isbn': '123456'}, headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Invalid JWT\n error body:'


def test_add_product_invalid_isbn_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service', side_effect=Exception)
    response = client.post('/api/cart/addProduct',
                           json={'cart_id': "edr46c09-4113-4155-950a-3560e5da4er0", 'isbn': '123456'})
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Invalid ISBN'


def test_remove_product_success(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.check_cart_id', return_value=True)
    mocker.patch('cartApp.database.renew_cart_expiry', return_value=sample_cart)
    mocker.patch('cartApp.database.delete_item',
                 return_value=sample_cart)

    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0', 'isbn': '123456'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'product removed from cart'
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_remove_product_success_logged_in_user(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.check_cart_id', return_value=True)
    mocker.patch('cartApp.database.renew_cart_expiry', return_value=sample_cart)
    mocker.patch('cartApp.database.delete_item', return_value=sample_cart)
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0', 'isbn': '123456'},
                             headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'product removed from cart'
    assert data['cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_remove_product_id_mismatch_exception_logged_in_user(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.check_cart_id', return_value=False)
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': 'art56c09-4113-4155-950a-3560e5da2ee0', 'isbn': '123456'},
                             headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID mismatch'
    assert data['cart_id'] == 'art56c09-4113-4155-950a-3560e5da2ee0'
    assert data['user_cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'


def test_remove_product_does_not_exist_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.check_cart_id', return_value=False)

    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': 'art56c09-4113-4155-950a-3560e5da2ee0', 'isbn': '123456'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart does not exist'
    assert data['cart_id'] == 'art56c09-4113-4155-950a-3560e5da2ee0'


def test_remove_product_id_not_provided_exception(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})

    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': None, 'isbn': '123456'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID not provided '


def test_remove_product_id_not_provided_exception_logged_in_user(client, mocker, sample_cart):
    # Mock external service calls and database functions
    mocker.patch('cartApp.call_service.get_product_from_external_service',
                 return_value={'title': 'Test Product', 'isbn': '123456', 'price': 100})
    mocker.patch('cartApp.database.check_cart_id', return_value=False)
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeProduct',
                             json={'cart_id': None, 'isbn': '123456'},
                             headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID not provided '


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


def test_show_cart_does_not_exist_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.check_cart_id', return_value=False)

    response = client.get('/api/cart/show_cart?cart_id=cart_id')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'cart ID does not exist '


def test_show_cart_id_not_provided_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.check_cart_id', return_value=False)

    response = client.get('/api/cart/show_cart')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID not provided '


def test_remove_cart(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.delete_cart', return_value=None)

    response = client.delete('/api/cart/removeCart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'cart deleted successfully'


def test_remove_cart_logged_in_user(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.delete_cart', return_value=None)
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeCart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'},
                             headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'cart deleted successfully'


def test_remove_cart_logged_in_user_no_id(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.delete_cart', return_value=None)
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeCart', json={'cart_id': None},
                             headers=headers)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['message'] == 'cart deleted successfully'


def test_remove_cart_id_not_provided_exception(client, mocker):
    # Mock database functions

    response = client.delete('/api/cart/removeCart', json={'cart_id': None})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID not provided '


def test_remove_cart_logged_in_user_id_mismatch_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.database.delete_cart', return_value=None)
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.check_for_user_cart', return_value='ace86c09-4113-4155-950a-3560e5da2ee0')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeCart', json={'cart_id': 'art86c09-4113-4155-950a-3560e5da2ee0'},
                             headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID mismatch'
    assert data['user_cart_id'] == 'ace86c09-4113-4155-950a-3560e5da2ee0'
    assert data['cart_id'] == 'art86c09-4113-4155-950a-3560e5da2ee0'


def test_remove_cart_logged_in_user_invalid_auth_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', side_effect=Exception)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.delete('/api/cart/removeCart', json={'cart_id': 'art86c09-4113-4155-950a-3560e5da2ee0'},
                             headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Invalid Authorization\n Error body:'


def test_link_cart_success(client, mocker):
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


def test_link_cart_id_not_provided_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.put('/api/cart/link-cart', json={'cart_id': None},
                          headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'cart ID not provided '


def test_link_cart_user_does_not_exist_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value=None)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.put('/api/cart/link-cart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'},
                          headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'user ID does not exist'


def test_link_cart_invalid_auth_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', side_effect=Exception)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.put('/api/cart/link-cart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'},
                          headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Invalid Authorization\n Error body:'


def test_link_cart_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.link_cart',
                 side_effect=Exception('No cart with this id exists or something went wrong'))
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.put('/api/cart/link-cart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'},
                          headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'No cart with this id exists or something went wrong'


def test_link_cart_missmatch_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value='user_id')
    mocker.patch('cartApp.database.link_cart', side_effect=Exception('You cannot link cart to another user'))
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }
    response = client.put('/api/cart/link-cart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'},
                          headers=headers)
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'You cannot link cart to another user'


def test_link_cart_no_auth_exception(client, mocker):
    # Mock database functions
    response = client.put('/api/cart/link-cart', json={'cart_id': 'ace86c09-4113-4155-950a-3560e5da2ee0'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'Invalid Request; No Authorization. This can only be called by an authorized entity'


def test_get_cart_success(client, mocker):
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


def test_get_cart_no_auth_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', side_effect=Exception)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }

    response = client.get('/api/cart/get_cart', headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'Invalid Authorization\n Error body:'


def test_get_cart_no_user_exception(client, mocker):
    # Mock database functions
    mocker.patch('cartApp.call_service.authenticate_user_with_jwt', return_value=None)
    headers = {
        'Authorization': 'Bearer your_jwt_token_here'
    }

    response = client.get('/api/cart/get_cart', headers=headers)
    assert response.status_code == 404
    data = json.loads(response.data)
    assert data['message'] == 'user ID does not exist'


def test_get_cart_exception(client):
    response = client.get('/api/cart/get_cart')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['message'] == 'Invalid Request; No Authorization. This can only be called by an authorized entity'
