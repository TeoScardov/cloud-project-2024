import json, datetime
from flask import current_app
from flask_jwt_extended import create_access_token, decode_token
from database import get_db

# Load accounts from file (to simulate a databse)
def load_accounts():
    print("Loading accounts")
    try:
        with open(current_app.config['DB_PATH'], 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save accounts to file
def save_accounts(accounts):
    print("Saving accounts")
    with open(current_app.config['DB_PATH'], 'w') as file:
        json.dump(accounts, file, indent=4)

# Check login credentials
def check_login_info(data):
    # Verify if data is valid
    if data is not None:
        # Verify username and password
        username = data.get('username', 'No username')
        password = data.get('password', 'No password')
        db = get_db()
        print(str(username in db))
        if username in db and db[username]['password'] == password:
            return create_access_token(identity=username, fresh=True, expires_delta=datetime.timedelta(12000))
    return None

# Register a new user if the name is available
def register_account(data):
    # Verify if data is valid
    if data is not None:
        # Get username and password
        username = data.get('username', None)
        password = data.get('password', None)
        # Check if the fields are valid
        if username == None or password == None:
            return 2
        # Add user to the in-memory db
        db = get_db()
        if username not in db:
            db[username] = {'password': password, 'role': 'user', 'suspended': 0,'info': ''}
            save_accounts(db)  # Save the updated db back to the file
            return 1
        else:
            return 0
    return 3

# Update the info of the account associated to the token
def update_account_info(token, data):
    # Get the user from the token
    if token is not None:
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        username = decode_token(token)['sub'] 
        # Get the updated information and modify the database entry
        new_info = data.get('info', {})
        db = get_db()
        if username in db:
            db[username]['info'] = new_info
            save_accounts(db)  # Update the file with new info
            return True
    return False

# Check if the token corresponds to an account in the database
def authenticate_token(token):
    # Get the user from the token
    if token is not None:
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
        username = decode_token(token)['sub'] 
        db = get_db()
        if username in db:
            return username, db[username]['role']
    return None, None