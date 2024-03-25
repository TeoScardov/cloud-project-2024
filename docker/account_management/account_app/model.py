import datetime
from flask import jsonify
from flask_jwt_extended import create_access_token, decode_token
from werkzeug.security import generate_password_hash, check_password_hash
from account_app.config import Config
from account_app.database import db
from account_app.dbmodel import *

'''# delete all accounts
def nuke():
    num_rows_deleted = db.session.query(Account).delete()
    db.session.commit()
    print(f"Deleted {num_rows_deleted} accounts.")'''

'''If not present, initialize the database with an admin user called admin1'''
def create_admin_user():
    try:
        if not Account.query.filter_by(username='admin1').first():
            admin_user = Account(
                username='admin1',
                password_hash=generate_password_hash(Config.ADMIN_PASSWORD),
                role='Admin',
                name='Admin',
                surname='User',
                suspended=False
            )
            db.session.add(admin_user)
            db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error creating admin user: {e}")

'''Register a new account, provided all the information. To create an account with higher priviledges, an admin JWT token has to be provided'''
def register_account(data, token=None):
    # Check if the username is available
    try:
        acc = Account.query.filter_by(username=data['username']).first()
        if acc is not None:
            return jsonify({"message": "Username already taken."}), 400
    except Exception as e:
        print(e)
        return jsonify({"message": "There was a problem with the database querying."}), 500
    
    new_account_role = "User"   # The default role for a new account
    try:
        # If a JWT token is provided, check if the registration request was made by an admin
        if token is not None:
            auth_msg, code = authenticate_token(token)
            if code != 200:     # If code == 200, the authentication was successful
                return auth_msg, code
            # Check the role
            if auth_msg.get_json()['role']  == "Admin": 
                new_account_role = data['role']
    except Exception as e:
        print(e)
        return jsonify({"message": "There was an error related to the authorization token."}), 400
    
    # Create the new account
    try:
        new_account = Account(
            username = data['username'],
            password_hash = generate_password_hash(data['password']),
            role = new_account_role, 
            suspended = False,
            name = data['name'],
            surname = data['surname']
        )
    except Exception as e:
        print(e)
        return jsonify({"message": "There was an error while parsing the data."}), 400

    try:
        db.session.add(new_account)
        db.session.commit()
        return jsonify({"message": "The registration was succesful."}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "There was an error in the database registration process."}), 500


'''Check login credentials given username and password'''
def check_login_info(data):
    # Verify that the data is valid
    if data is not None:
        # Get username and password
        username = data.get('username', None)
        password = data.get('password', None)
        # Query the db to check if the username exists
        try:
            acc = Account.query.filter_by(username=username).first()
        except Exception as e:
            print(e)
            return jsonify({"message": "There was a problem with the db querying."}), 500
        # Check the query result
        if acc == None:
            return jsonify({"message": "Username not found."}), 400
        # Check that the password matches
        if check_password_hash(acc.password_hash, password):
            # Password matches, authentication successful
            token_ttl = Config.JWT_TOKEN_TTL
            token = create_access_token(identity=username, fresh=True, expires_delta=datetime.timedelta(token_ttl))
            return jsonify({"message": "Login successful.", "access_token" : token}), 200
        # Authentication failed
        return jsonify({"message": "The password is not correct."}), 400


'''Update the information of the account specified in the json. This could be either requested by a user to update their own account, or by an admin to update any account'''
def update_account_info(token, data): 
    # Provided a JWT token, get the username and role of the account that is requesting the modification
    auth_msg, code = authenticate_token(token)
    if code != 200:     # If code == 200, the authentication was successful
        return auth_msg, code
    token = token.split(' ')[1]     # The auth token is in the form "Bearer <token_string>"
    requesting_username = auth_msg.get_json()['username']
    requesting_role = auth_msg.get_json()['role']
    # Get the username of the account that will be modified
    username = data.get('username', None)
    if username is None:
        return jsonify({"message": "The request must specify the username of the account to change its information."}), 400
    
    # Modify the account
    try:
        # tbu stands for "to be updated"
        account_tbu = Account.query.filter_by(username=username).first()
        if account_tbu is None:
            # the account isn't in the DB
            return jsonify({"message": "Username not found."}), 500
        # The request could be either made by the owner of the account or by an admin
        if (requesting_username == account_tbu.username) or (requesting_role == "Admin"):
            # Updates with low priviledges
            if 'password' in data:
                account_tbu.password_hash = generate_password_hash(data['password'])
            if 'name' in data:
                account_tbu.name = data['name']
            if 'surname' in data:
                account_tbu.surname = data['surname']
            # Updates with high priviledges
            if requesting_role == "Admin":
                if 'suspended' in data:
                    account_tbu.suspended = (data['suspended'] == True)
            db.session.commit()
            return jsonify({"message": "Account information updated."}), 200
    except Exception as e:
        print(e)
        db.session.rollback()
        return jsonify({"message": "The account information could not be updated."}), 500


'''Check if the token corresponds to an account in the database and return its id, username, and role'''
def authenticate_token(token):
    if token is None:
        return jsonify({"message": "Token not valid"}), 400
    # Get the username from the token
    try:
        token = token.split(' ')[1]     # The token is in the form "Bearer <token string>"
        username = decode_token(token)['sub']
    except Exception as e:
        print(e)
        return jsonify({"message": "Token not valid"}), 400
    
    # Query the database to obtain the id and role of the requesting account
    try:
        account = Account.query.filter_by(username=username).first()
        if account is None:     # No account was found
            return jsonify({"message": "Account not found."}), 400
        id_ = account.id
        role = account.role.value   # role is an Enum
        return jsonify({"message": "User authenticated", "id": id_, "username": username, "role": role}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "There was a problem with the database querying."}), 500