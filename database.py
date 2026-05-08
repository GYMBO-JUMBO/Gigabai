import json
import os

DB_FILE = "users.json"

def load_users():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    users = load_users()
    if username in users:
        return False, "User already exists"
    users[username] = {
        "password": password,
        "balance": 0.0,
        "income": 0.0,
        "expenses": 0.0,
        "transactions": [],
        "first_name": "",
        "last_name": "",
        "workplace": "",
        "bank_name": "",
        "account_number": "",
        "theme": "dark"
    }
    save_users(users)
    return True, "Registered successfully"

def login_user(username, password):
    users = load_users()
    if username not in users:
        return False, "User not found"
    if users[username]["password"] != password:
        return False, "Incorrect password"
    return True, users[username]

def get_user(username):
    users = load_users()
    return users.get(username, None)

def update_user(username, data):
    users = load_users()
    if username in users:
        users[username].update(data)
        save_users(users)