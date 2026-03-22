# 📓 Notepad — Personal Notes Web App

A full-stack notes app with user accounts, built with Python (Flask) + HTML/CSS/JS.

## Features
- ✅ Register & login with username + password
- ✅ Write notes directly in the browser
- ✅ Upload `.txt` files as notes
- ✅ View, browse, and delete notes
- ✅ Notes are stored per-user in a JSON file
- ✅ Passwords hashed with SHA-256
- ✅ Keyboard shortcut: `Ctrl+Enter` to save

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the server
```bash
python app.py
```

### 3. Open in browser
Visit: http://localhost:5000

## Project Structure
```
notes_app/
├── app.py              # Flask backend (API + static serving)
├── requirements.txt    # Python dependencies
├── data/
│   └── db.json         # User accounts + notes (auto-created)
└── static/
    └── index.html      # Full frontend (HTML + CSS + JS)
```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/register | Create new account |
| POST | /api/login | Authenticate user |
| GET  | /api/notes/:user | Get all notes |
| POST | /api/notes/:user | Save a new note |
| DELETE | /api/notes/:user/:id | Delete a note |

## Notes on Security
- Passwords are hashed before storage (SHA-256)
- Each API request requires the password hash as `X-Auth` header
- For production use, consider adding HTTPS, session tokens, and rate limiting
