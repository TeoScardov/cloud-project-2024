import json
# Load users from file at startup
def load_users():
    try:
        with open('../userservice/users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save users to file
def save_users(users_db):
    with open('../userservice/users.json', 'w') as file:
        json.dump(users_db, file, indent=4)