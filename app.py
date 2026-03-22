from flask import Flask, request, jsonify, send_from_directory
import json
import os
import hashlib
import uuid
from datetime import datetime

app = Flask(__name__, static_folder='static')

DB_FILE = 'data/db.json'

def load_db():
    if not os.path.exists(DB_FILE):
        os.makedirs('data', exist_ok=True)
        save_db({'users': {}, 'notes': {}})
    with open(DB_FILE, 'r') as f:
        return json.load(f)

def save_db(db):
    os.makedirs('data', exist_ok=True)
    with open(DB_FILE, 'w') as f:
        json.dump(db, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400
    if len(password) < 4:
        return jsonify({'error': 'Password must be at least 4 characters'}), 400
    db = load_db()
    if username in db['users']:
        return jsonify({'error': 'Username already taken'}), 409
    db['users'][username] = {
        'password': hash_password(password),
        'created_at': datetime.now().isoformat()
    }
    db['notes'][username] = []
    save_db(db)
    return jsonify({'message': 'Account created successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    db = load_db()
    user = db['users'].get(username)
    if not user or user['password'] != hash_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    return jsonify({'message': 'Login successful', 'username': username})

@app.route('/api/notes/<username>', methods=['GET'])
def get_notes(username):
    password_hash = request.headers.get('X-Auth')
    db = load_db()
    user = db['users'].get(username)
    if not user or user['password'] != password_hash:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify({'notes': db['notes'].get(username, [])})

@app.route('/api/notes/<username>', methods=['POST'])
def upload_note(username):
    password_hash = request.headers.get('X-Auth')
    db = load_db()
    user = db['users'].get(username)
    if not user or user['password'] != password_hash:
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    if not content:
        return jsonify({'error': 'Note content cannot be empty'}), 400
    note = {
        'id': str(uuid.uuid4()),
        'title': title or 'Untitled',
        'content': content,
        'created_at': datetime.now().isoformat()
    }
    db['notes'][username].insert(0, note)
    save_db(db)
    return jsonify({'message': 'Note saved', 'note': note})

@app.route('/api/notes/<username>/<note_id>', methods=['DELETE'])
def delete_note(username, note_id):
    password_hash = request.headers.get('X-Auth')
    db = load_db()
    user = db['users'].get(username)
    if not user or user['password'] != password_hash:
        return jsonify({'error': 'Unauthorized'}), 401
    db['notes'][username] = [n for n in db['notes'].get(username, []) if n['id'] != note_id]
    save_db(db)
    return jsonify({'message': 'Note deleted'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
