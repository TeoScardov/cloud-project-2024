import datetime
from flask_jwt_extended import create_access_token, decode_token
from sqlalchemy.orm.attributes import flag_modified
from werkzeug.security import generate_password_hash, check_password_hash
from accountApp.config import Config
from accountApp.database import db
from accountApp.dbmodel import *

'''Register a new account. To create an account with higher priviledges, an admin JWT token has to be provided'''
def register_account(data, token=None):
    # Check if username and e-mail address are available
    try:
        acc = Account.query.filter_by(username=data['username']).first()
        if acc:
            return {"message": "Username already taken."}, 400
        acc = Account.query.filter_by(email_address=data['email_address']).first()
        if acc:
            return {"message": "E-mail address already in use."}, 400
    except Exception as e:
        print(e)
        return {"message": "There was a problem with the database querying."}, 500

    new_account_role = "USER"   # The default role for a new account
    try:
        # If a JWT token is provided, check if the registration request was made by an admin
        if token:
            auth_msg, code = authenticate_token(token)
            if code != 200:
                return auth_msg, code   # The authentication was not successful
            # Check the role
            if auth_msg['role'] == "ADMIN": 
                new_account_role = data['role']
    except Exception as e:
        print(e)
        return {"message": "There was an error related to the authorization token."}, 400

    # Create the new account
    try:
        new_account = Account(
            email_address = data['email_address'],
            username = data['username'],
            password_hash = generate_password_hash(data['password']),
            name = data['name'],
            surname = data['surname'],
            role = new_account_role
        )
    except Exception as e:
        print(e)
        return {"message": "There was an error while parsing the data."}, 400
    
    # Add the account to the database
    try:
        db.session.add(new_account)
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
        return {"message": "There was an error in the database registration process for the account."}, 500
    
    # Create the customer entry in the database
    if new_account_role == "USER":
        try:
            new_customer = Customer(
                account_id = new_account.id,
                library = [],
                phone_number = None,
                billing_address = None
            )
            db.session.add(new_customer)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"message": "There was an error in the database registration process for the customer."}, 500
    return {"message": "The registration was succesful."}, 200


'''Check login credentials given username (or email) and password'''
def check_login_info(data):
    # Get login credentials
    email = data.get('email_address', None)
    username = data.get('username', None)
    password = data.get('password', None)
    # Query the db to check if the username or email exist
    try:
        acc = Account.query.filter_by(username=username).first()
        if not acc:
            acc = Account.query.filter_by(email_address=email).first()
    except Exception as e:
        print(e)
        return {"message": "There was a problem with the database querying."}, 500
    # Check the query result
    if not acc:
        return {"message": "Account not found."}, 400
    
    # Check that the account has not been suspended
    if acc.suspended:
        return {"message": "The account was suspended."}, 400

    # Check that the password matches
    if check_password_hash(acc.password_hash, password):
        # Password matches, authentication successful
        token_ttl = Config.JWT_TOKEN_TTL
        token = create_access_token(identity=acc.id, fresh=True, expires_delta=datetime.timedelta(token_ttl))
        return {"message": "Login successful.", "access_token" : token}, 200
    # Authentication failed
    return {"message": "The password is not correct."}, 400


'''Update the information of the account specified in the json. This could be either requested by a user to update their own account, or by an admin to update any account'''
def update_info(token, data): 
    # Provided a JWT token, get the id and role of the account that is requesting the modification
    auth_msg, code = authenticate_token(token)
    if code != 200:
        return auth_msg, code   # The authentication was not successful
    requesting_account_id = auth_msg['account_id']
    requesting_role = auth_msg['role']

    updating_account_id = data.get('account_id', None)
    # Modify the account
    try:
        updating_account = Account.query.filter_by(id=updating_account_id).first()
        if not updating_account:
            # the account isn't in the DB
            return {"message": "Account id not valid."}, 400
        # The request could be either made by the owner of the account or by an admin
        if (requesting_account_id == updating_account.id) or (requesting_role == "ADMIN"):
            # Account updates with low priviledges
            if 'password' in data:
                updating_account.password_hash = generate_password_hash(data['password'])
            if 'name' in data:
                updating_account.name = data['name']
            if 'surname' in data:
                updating_account.surname = data['surname']
            # Updates with high priviledges
            if requesting_role == "ADMIN":
                if 'suspended' in data:
                    updating_account.suspended = data['suspended']
            # Customer updates
            if updating_account.role.value == "USER":
                updating_customer = Customer.query.filter_by(account_id=updating_account_id).first()
                if 'library' in data:
                    new_library = updating_customer.library
                    if not new_library: # The library could be empty
                        new_library = []
                    if 'add' in data['library']:
                        for new_book in data['library']['add']:
                            new_library.append(new_book)
                    if 'delete' in data['library']:
                        for book in data['library']['delete']:
                            if book in new_library:
                                new_library.remove(book)
                    updating_customer.library = new_library
                    flag_modified(updating_customer, "library")
                if 'phone_number' in data:
                    updating_customer.phone_number = data['phone_number']
                if 'billing_address' in data:
                    updating_customer.billing_address = data['billing_address']
            db.session.commit()
            return {"message": "Info successfully updated."}, 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return {"message": "The info could not be updated."}, 500


'''Check if the token corresponds to an account in the database and return its information'''
def authenticate_token(token):
    # Get the account id from the token
    try:
        token = token.split(' ')[1]     # The token is in the form "Bearer <token_string>"
        account_id = decode_token(token)['sub']
    except Exception as e:
        print(e)
        return {"message": "Token not valid"}, 400
    
    # Query the database to obtain the information about the requesting account
    try:
        account = Account.query.filter_by(id=account_id).first()
        if not account:     # Account not found
            return {"message": "Account not found."}, 400
        # Return also the customer id (only for USERs)
        customer_id = None
        if account.role.value == "USER":
            customer = Customer.query.filter_by(account_id=account_id).first()
            customer_id = customer.id
        return {"message": "Account successfully authenticated", 
                "account_id": account.id, 
                "customer_id": customer_id,                
                "username": account.username, 
                "role": account.role.value,   # role is an Enum
                "suspended": account.suspended
                }, 200
    except Exception as e:
        print(e)
        return {"message": "There was a problem with the database querying."}, 500
    

'''Return all the info of the account specified in the JWT token'''
def get_info(token):
    auth_msg, code = authenticate_token(token)
    try:
        account = Account.query.filter_by(id=auth_msg['account_id']).first()
        account_info = {
        "id": account.id,
        "email_address": account.email_address,
        "username": account.username,
        "name": account.name,
        "surname": account.surname,
        "role": account.role.value,
        "suspended": account.suspended
        }
        if account.role.value == "USER":
            customer = Customer.query.filter_by(account_id=auth_msg['account_id']).first()
            account_info['library'] = customer.library
            account_info['phone_numer'] = customer.phone_number
            account_info['billing_address'] = customer.billing_address
    except Exception as e:
        print(e)
        return {"message": "Error."}, 400
    return account_info, 200