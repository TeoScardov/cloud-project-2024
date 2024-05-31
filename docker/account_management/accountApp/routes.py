from flask import request, jsonify
from flask_jwt_extended import jwt_required
from . import account, model

# /api/account
@account.route('/')
def index():
    """
    This is an endpoint that returns a simple welcome message
    ---
    responses:
        200:
            description: A welcome message
    """
    return jsonify({"message": "Welcome to the account service API section."}), 200



@account.route("/health")
def health():
    """
    This is an endpoint that returns 'UP'
    ---
    responses:
        200:
            description: The string 'UP'
    """
    return jsonify({"status": "UP"}), 200



@account.route('/register', methods=['POST'])
def register():
    """
    Register a new account. To create an account with higher privileges, an admin JWT token has to be provided.
    ---
    parameters:
      - name: Authorization
        in: header
        required: false
        type: string
        description: JWT Bearer Token for authorization. It is only needed if an admin is creating an account with higher privileges. The expected format is 'Bearer [token]'.
      - name: data
        in: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    description: The username of the new account.
                email_address:
                    type: string
                    description: The email of the new account.
                password:
                    type: string
                    description: The password of the new account.
                name:
                    type: string
                    description: The name associated with the new account.
                surname:
                    type: string
                    description: The surname associated with the new account.
                role:
                    type: string
                    enum: [USER, EMPLOYEE, ADMIN]
                    description: The role of the new account (it only needs to be specified when the account is created by an admin).
    responses:
        200:
            description: Account successfully registered.
        400:
            description: Username or email address already taken, or error related to the authorization token.
        500:
            description: There was a problem with the database querying.
    """
    # Parse JSON data sent with the request
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "There was a problem with the json file."}), 400
    # Retrieve the JWT token, if present
    token = request.headers.get('Authorization', None)
    # Register the new account in the database
    message, code = model.register_account(data, token)
    return jsonify(message), code



@account.route('/login', methods=['POST'])
def login():
    """
    Check login credentials given username (or email) and password.
    ---
    parameters:
      - name: data
        in: body
        required: true
        schema:
            type: object
            properties:
                username:
                    type: string
                    description: The username of the account to login into (this and the email can  be used interchangeably).
                email_address:
                    type: string
                    description: The email of the account to login into (this and the username can  be used interchangeably).
                password:
                    type: string
                    description: The password of the account to login into.
    responses:
        200:
            description: Login successful.
        400:
            description: Invalid username or password, or the account was suspended, or the password was wrong.
        500:
            description: There was a problem with the database querying.
    """
    # Parse JSON data sent with the request
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "There was a problem with the json file."}), 400
    # Check login credentials, return the access token if the login is successful
    message, code = model.check_login_info(data)
    return jsonify(message), code



@account.route('/logout', methods=['POST'])
@jwt_required(fresh=True)
def logout():
    """
    To log out, discard the client-side JWT token (to be implemented in the front-end).
    ---
    responses:
        200:
            description: A logout message.
    """
    return jsonify({"message": "Logged out."}), 200



@account.route('/update', methods=['POST'])
@jwt_required(fresh=True)
def update():
    """
    Update the information of the account specified in the JSON. This could be either requested by a user to update their own account, or by an admin to update any account.
    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: JWT Bearer Token for authorization.
      - name: data
        in: body
        required: true
        schema:
            type: object
            properties:
                account_id:
                    type: integer
                    description: The ID of the account to be updated (admin only).
                username:
                    type: string
                    description: The username of the account to be updated (admin only).
                password:
                    type: string
                    description: New password for the account.
                name:
                    type: string
                    description: New name for the account.
                surname:
                    type: string
                    description: New surname for the account.
                suspended:
                    type: boolean
                    description: Suspension status of the account (admin only).
                library:
                    type: object
                    properties:
                        add:
                            type: array
                            items:
                                type: string
                            description: List of books to add to the library.
                        delete:
                            type: array
                            items:
                                type: string
                            description: List of books to remove from the library.
                phone_number:
                    type: string
                    description: New phone number for the account.
                billing_address:
                    type: string
                    description: New billing address for the account.
                cc:
                    type: string
                    description: New credit card number for the account.
                expiredate:
                    type: string
                    description: New credit card expiration date for the account.
                cvv:
                    type: string
                    description: New credit card CVV for the account.
    responses:
        200:
            description: Info successfully updated.
        400:
            description: Account ID not valid.
        500:
            description: There was a problem with the database querying or updating the info.
    """

    # Parse JSON data sent with the request
    try:
        data = request.get_json()
    except:
        return jsonify({"message": "There was a problem with the json file."}), 400
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # The info could be updated by the owner of the account, or by an admin
    message, code = model.update_info(token, data)
    return jsonify(message), code



@account.route('/authenticate', methods=['POST'])
@jwt_required()
def authenticate():
    """
    Check if the token corresponds to an account in the database and return its information.
    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: JWT Bearer Token for authorization.
    responses:
        200:
            description: Account successfully authenticated.
            schema:
                type: object
                properties:
                    message:
                        type: string
                        example: "Account successfully authenticated."
                    account_id:
                        type: integer
                    customer_id:
                        type: integer
                        nullable: true
                    username:
                        type: string
                    role:
                        type: string
                        enum: [USER, EMPLOYEE, ADMIN]
                    suspended:
                        type: boolean
        400:
            description: Token not valid or account not found.
        500:
            description: There was a problem with the database querying.
    """
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # Get the username and role associated to the JWT token
    message, code = model.authenticate_token(token)
    return jsonify(message), code



@account.route('/info', methods=['POST'])
@jwt_required(fresh=True)
def info():
    """
    Return all the info of the account specified in the JWT token (or in the JSON body if the request is made by an admin account).
    ---
    parameters:
      - name: Authorization
        in: header
        required: true
        type: string
        description: JWT Bearer Token for authorization.
      - name: data
        in: body
        required: false
        schema:
            type: object
            properties:
                account_id:
                    type: integer
                    description: The ID of the account to retrieve info for (admin only).
                username:
                    type: string
                    description: The username of the account to retrieve info for (admin only).
    responses:
        200:
            description: Information successfully retrieved.
            schema:
                type: object
                properties:
                    id:
                        type: integer
                    email_address:
                        type: string
                    username:
                        type: string
                    name:
                        type: string
                    surname:
                        type: string
                    role:
                        type: string
                        enum: [USER, EMPLOYEE, ADMIN]
                    suspended:
                        type: boolean
                    library:
                        type: array
                        items:
                            type: string
                            nullable: true
                    phone_number:
                        type: string
                        nullable: true
                    billing_address:
                        type: string
                        nullable: true
                    cc:
                        type: string
                        nullable: true
                    expiredate:
                        type: string
                        nullable: true
                    cvv:
                        type: string
                        nullable: true
        400:
            description: Account ID or username not valid.
        500:
            description: There was a problem with the database querying.
    """
    # Retrieve the json data, if present (otherwise it is set to None)
    data = request.get_json(silent=True)
    # Retrieve the JWT token
    token = request.headers.get('Authorization', None)
    # Register the new account in the database
    message, code = model.get_info(data, token)
    return jsonify(message), code