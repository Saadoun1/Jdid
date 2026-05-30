import sqlite3
from datetime import datetime
import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

DB_PATH = Path(os.environ.get("DATABASE_PATH", Path(__file__).with_name("database.db")))
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin")


def get_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_db() as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/submit")
def submit():
    name = request.form.get("name", "").strip()
    if not name:
        return render_template("index.html", error="Please enter your name.")

    with get_db() as db:
        db.execute(
            "INSERT INTO entries (name, created_at) VALUES (?, ?)",
            (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        )

    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password", "")
        if password == ADMIN_PASSWORD:
            session["is_admin"] = True
            return redirect(url_for("admin"))

        return render_template("login.html", error="Wrong password.")

    return render_template("login.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.get("/admin")
def admin():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    with get_db() as db:
        entries = db.execute(
            "SELECT id, name, created_at FROM entries ORDER BY id DESC"
        ).fetchall()

    return render_template("admin.html", entries=entries)


init_db()


if __name__ == "__main__":
    app.run(debug=True)
