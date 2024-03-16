from utility import generate_ttl
from models import db, Cart, CartItem, Product


def insert_cart(total, user_id):
    new_cart = Cart(user_id=user_id, total=total, exp_date=generate_ttl(3))
    # Add the new_cart to the session and commit to the database
    db.session.add(new_cart)
    db.session.commit()
    return new_cart.cart_id


def insert_item(cart_id, product_id, name, quantity, price):
    new_item = CartItem(cart_id=cart_id, product_id=product_id, name=name, quantity=quantity, price=price)
    # Add the new_cart to the session and commit to the database
    db.session.add(new_item)
    db.session.commit()


def check_cart_id(cart_id):
    cart = Cart.query.filter_by(cart_id=cart_id).first()
    return cart is not None


def add_item(cart_id, item, user_id):
    # Retrieve existing cart items and total
    existing_items = CartItem.query.filter_by(cart_id=cart_id).with_entities(CartItem.product_id).all()
    item_id = item['product_id']
    existing_product_ids = [existing_item[0] for existing_item in existing_items]
    if item_id in existing_product_ids:
        # update existing item
        cart_item_to_update = CartItem.query.filter_by(cart_id=cart_id, product_id=item_id).first()
        cart_item_to_update.quantity += 1
        db.session.commit()
    else:
        # add new item
        insert_item(cart_id, item_id, item['name'], 1, item['price'])

    return update_total_price(cart_id, user_id)


def delete_item(cart_id, item, user_id):
    item_id = item['product_id']
    cart_item_to_modify = CartItem.query.filter_by(cart_id=cart_id, product_id=item_id).first()
    if cart_item_to_modify:
        if cart_item_to_modify.quantity == 1:
            # delete the item
            db.session.delete(cart_item_to_modify)
            db.session.commit()
        elif cart_item_to_modify.quantity > 1:
            # change the quantity
            cart_item_to_modify.quantity = cart_item_to_modify.quantity - 1
            db.session.commit()

    return update_total_price(cart_id, user_id)


def update_total_price(cart_id, user_id):
    # Retrieve new cart items price and quantity
    selected_items = CartItem.query.filter_by(cart_id=cart_id).with_entities(
        CartItem.product_id,
        CartItem.price,
        CartItem.quantity
    ).all()

    # Calculate the updated_total
    updated_total = 0
    for item in selected_items:
        product_id, price, quantity = item
        updated_total += price * quantity
    # Update the total in the cart
    if user_id is not None:
        Cart.query.filter_by(cart_id=cart_id).update({'total': updated_total, 'user_id': user_id})
    else:
        Cart.query.filter_by(cart_id=cart_id).update({'total': updated_total})
    db.session.commit()
    return Cart.query.filter_by(cart_id=cart_id).first()


def renew_cart_expiry(cart_id, user_id):
    if user_id is not None:
        Cart.query.filter_by(cart_id=cart_id).update({'exp_date': generate_ttl(3), 'user_id': user_id})
    else:
        Cart.query.filter_by(cart_id=cart_id).update({'exp_date': generate_ttl(3)})
    db.session.commit()
    return Cart.query.get(cart_id)


def get_product_by_id(product_id):
    return Product.query.filter_by(product_id=product_id).first()


def get_cart_items_by_cart_id(cart_id):
    cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
    if cart_items:
        # Convert the list of cart items to a list of dictionaries
        cart_items_list = [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'name': item.name,
            'price': item.price,
            # Include other fields as needed
        } for item in cart_items]

        return cart_items_list


def merge_carts(user_id):
    existing_carts_id = Cart.query.filter_by(user_id=user_id).with_entities(Cart.cart_id).all()
    # Extract cart IDs from the result
    cart_ids = [existing_carts_id[0] for cart_id in existing_carts_id]
    new_cart_id = insert_cart(0, user_id)
    for cart_id in cart_ids:
        CartItem.query.filter_by(cart_id=cart_id).update({'cart_id': new_cart_id})
        Cart.query.filter_by(user_id=user_id, cart_id=cart_id).delete()

    # Retrieve new cart items price and quantity
    selected_items = CartItem.query.filter_by(cart_id=new_cart_id).with_entities(
        CartItem.price,
        CartItem.quantity
    ).all()

    # Calculate the updated_total
    updated_total = 0
    for item in selected_items:
        price, quantity = item
        updated_total += price * quantity

    # Update the total in the cart
    Cart.query.filter_by(cart_id=new_cart_id).update({'total': updated_total})

    db.session.commit()
    return Cart.query.get(new_cart_id)


def check_for_user_cart(user_id):
    existing_carts = Cart.query.filter_by(user_id=user_id).all()
    if len(existing_carts) > 1:
        return merge_carts(user_id).cart_id
    elif len(existing_carts) == 1:
        return existing_carts[0].cart_id
    else:
        return None
