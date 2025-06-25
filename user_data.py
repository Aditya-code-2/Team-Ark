import json
import os

DB_FILE = 'users.json'

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(DB_FILE, 'w') as f:
        json.dump(users, f)
        f.write('\n')  # after every data breakline

# At the top of your Flask app
users = load_users()

# In your /register route, after updating users:
save_users(users)

#Make sure users.json is:
#In your .gitignore if you're using Git Not directly exposed to the web (don’t put it in /static or /templates)
