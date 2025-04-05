
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/register", methods=["POST"])
def register():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                    (username,  hashed_pw))
        conn.commit()
        return jsonify({"msg": "Registration successful!"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route("/login", methods=["POST"])
def login():
    data = request.form
    username = data.get("username")
    password = data.get("password")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row[0]):
        return jsonify({"msg": "Login successful!"}), 200
    return jsonify({"error": "Invalid username or password"}), 401

if __name__ == "__main__":
    app.run(debug=True)
