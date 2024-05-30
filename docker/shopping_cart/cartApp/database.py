from .models import db, Cart, CartItem
from .utility import generate_ttl


def insert_cart(total, user_id):
    new_cart = Cart(user_id=user_id, total=total, exp_date=generate_ttl(3))
    # Add the new_cart to the session and commit to the database
    db.session.add(new_cart)
    db.session.commit()
    return new_cart.id


def insert_item(cart_id, isbn, title, price):
    new_item = CartItem(cart_id=cart_id, isbn=isbn, title=title,  price=price)
    # Add the new_cart to the session and commit to the database
    db.session.add(new_item)
    db.session.commit()


def check_cart_id(cart_id):
    cart = Cart.query.filter_by(id=cart_id).first()
    return cart is not None


def add_item(cart_id, item, user_id):
    # Retrieve existing cart items and total
    existing_items = CartItem.query.filter_by(cart_id=cart_id).with_entities(CartItem.isbn).all()
    item_id = item['isbn']
    existing_ids = [existing_item[0] for existing_item in existing_items]
    if item_id in existing_ids:
        raise Exception('Item already exists in cart, you cannot add each item more than once')
    else:
        # add new item
        insert_item(cart_id, item_id, item['title'], item['price'])

    return update_total_price(cart_id, user_id)


def delete_item(cart_id, item, user_id):
    item_id = item['isbn']
    cart_item_to_modify = CartItem.query.filter_by(cart_id=cart_id, isbn=item_id).first()
    if cart_item_to_modify:
        db.session.delete(cart_item_to_modify)
        db.session.commit()
        return update_total_price(cart_id, user_id)
    else:
        raise Exception('Item not found')


def update_total_price(cart_id, user_id):
    # Retrieve new cart items price
    selected_items = CartItem.query.filter_by(cart_id=cart_id).with_entities(
        CartItem.isbn,
        CartItem.price,
    ).all()

    # Calculate the updated_total
    updated_total = 0
    for item in selected_items:
        isbn, price = item
        updated_total += price
    # Update the total in the cart
    if user_id is not None:
        Cart.query.filter_by(id=cart_id).update({'total': updated_total, 'user_id': user_id})
    else:
        Cart.query.filter_by(id=cart_id).update({'total': updated_total})
    db.session.commit()
    return Cart.query.filter_by(id=cart_id).first()


def renew_cart_expiry(cart_id, user_id):
    if user_id is not None:
        Cart.query.filter_by(id=cart_id).update({'exp_date': generate_ttl(3), 'user_id': user_id})
    else:
        Cart.query.filter_by(id=cart_id).update({'exp_date': generate_ttl(3)})
    db.session.commit()
    return Cart.query.get(cart_id)


def get_cart_items_by_cart_id(cart_id):
    cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
    if cart_items:
        # Convert the list of cart items to a list of dictionaries
        cart_items_list = [{
            'isbn': item.isbn,
            'title': item.title,
            'price': item.price,
        } for item in cart_items]

        return cart_items_list


def delete_old_carts(user_id, req_cart_id):
    existing_carts = Cart.query.filter_by(user_id=user_id).all()
    # Delete all other carts
    for cart in existing_carts:
        if str(cart.id) != req_cart_id:
            db.session.delete(cart)

    # Commit the changes to the database
    db.session.commit()

    return Cart.query.filter_by(user_id=user_id).first()


def check_for_user_cart(user_id, req_cart_id):
    existing_carts = Cart.query.filter_by(user_id=user_id).all()
    if len(existing_carts) > 1:
        result = delete_old_carts(user_id, req_cart_id)
        return result.id if result else None
    elif len(existing_carts) == 1:
        return existing_carts[0].id
    else:
        return None


def delete_cart(cart_id):
    cart_to_delete = Cart.query.get(cart_id)
    if cart_to_delete:
        db.session.delete(cart_to_delete)
        db.session.commit()


def link_cart(cart_id, user_id):
    delete_old_carts(user_id, cart_id)
    cart_to_link = Cart.query.filter_by(id=cart_id).first()
    if cart_to_link and cart_to_link.user_id == user_id:
        return cart_to_link
    elif cart_to_link and cart_to_link.user_id is not None and cart_to_link.user_id != user_id:
        raise Exception("You can't link cart to another user")
    elif cart_to_link and cart_to_link.user_id is None:
        Cart.query.filter_by(id=cart_id).update({'user_id': user_id})
        db.session.commit()
        return cart_to_link
    else:
        raise Exception("No cart with this id exists or something went wrong")
