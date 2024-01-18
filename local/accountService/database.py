import json

db = None

def init_db(app):
    global db
    try:
        with open(app.config['DB_PATH'], 'r') as file:
            db = json.load(file)
            print("Initializing accounts")
    except FileNotFoundError:
        db = {}
        print("Failed to initialize accounts")

def get_db():
    if db is None:
        raise Exception("Database not initialized")
    return db
