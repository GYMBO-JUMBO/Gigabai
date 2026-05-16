import json
import os
from datetime import datetime

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
        "categories": {},
        "income_history": [],
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

def add_income(username, amount, source="Salary", note=""):
    users = load_users()
    if username not in users:
        return False
    user = users[username]
    if "income_history" not in user:
        user["income_history"] = []
    user["income_history"].append({
        "amount": amount,
        "source": source,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    total_income = sum(t["amount"] for t in user["income_history"])
    user["income"] = total_income
    user["balance"] = total_income - user.get("expenses", 0.0)
    save_users(users)
    return True

def add_category_expense(username, category, amount, note=""):
    users = load_users()
    if username not in users:
        return False
    user = users[username]
    if "categories" not in user:
        user["categories"] = {}
    if category not in user["categories"]:
        user["categories"][category] = []
    user["categories"][category].append({
        "amount": amount,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    })
    total_expenses = sum(
        sum(t["amount"] for t in txns)
        for txns in user["categories"].values()
    )
    user["expenses"] = total_expenses
    user["balance"] = user.get("income", 0.0) - total_expenses
    save_users(users)
    return True

def delete_transaction(username, category, date):
    """Delete a specific transaction by category and date."""
    users = load_users()
    if username not in users:
        return False
    user = users[username]
    cats = user.get("categories", {})
    if category in cats:
        cats[category] = [t for t in cats[category] if t.get("date") != date]
        if not cats[category]:
            del cats[category]
    user["categories"] = cats
    total_expenses = sum(
        sum(t["amount"] for t in txns)
        for txns in cats.values()
    )
    user["expenses"] = total_expenses
    user["balance"] = user.get("income", 0.0) - total_expenses
    save_users(users)
    return True