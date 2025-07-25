# routes/journal.py

import sqlite3
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
import os

journal_bp = Blueprint("journal", __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'mindcare.db')

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS journals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                entry TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

init_db()

# 📝 POST /journal - Add a new journal entry
@journal_bp.route("/journal", methods=["POST"])
def add_journal_entry():
    data = request.get_json()
    user_id = data.get("user_id")
    entry = data.get("entry")

    if not user_id or not entry:
        return jsonify({"error": "Missing user_id or entry"}), 400

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO journals (user_id, entry) VALUES (?, ?)", (user_id, entry))
        conn.commit()

    return jsonify({"message": "Entry added successfully!"})

# 📖 GET /journal/<user_id> - Get all entries of a user
@journal_bp.route("/journal/<user_id>", methods=["GET"])
def get_entries(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT entry, timestamp FROM journals WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        entries = cursor.fetchall()

    formatted = [{"entry": e, "timestamp": t} for e, t in entries]
    return jsonify({"entries": formatted})


# 🔥 GET /journal/<user_id>/streak - Get user’s journaling streak
@journal_bp.route("/journal/<user_id>/streak", methods=["GET"])
def get_streak(user_id):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DATE(timestamp) FROM journals WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
        dates = [row[0] for row in cursor.fetchall()]

    if not dates:
        return jsonify({"streak": 0})

    streak = 1
    today = datetime.today().date()

    for i in range(1, len(dates)):
        prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d").date()
        curr_date = datetime.strptime(dates[i], "%Y-%m-%d").date()
        if (prev_date - curr_date).days == 1:
            streak += 1
        else:
            break

    if datetime.strptime(dates[0], "%Y-%m-%d").date() != today:
        streak = 0

    return jsonify({"streak": streak})
