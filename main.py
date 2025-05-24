import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from src.utils.logger import setup_logger
from src.utils.supabase_client import SupabaseClient
from src.utils.openai_handler import OpenAIHandler
from src.utils.chat_history import ChatHistory
from datetime import datetime

load_dotenv()

# Verify required environment variables
required_vars = ["SUPABASE_URL", "SUPABASE_KEY", "OPENAI_API_KEY"]
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please create a .env file with the required variables.")
    exit(1)

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

setup_logger()

supabase = SupabaseClient()
openai_handler = OpenAIHandler()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        if not email or not password:
            flash("Please enter both email and password.", "warning")
            return render_template("login.html")
        try:
            user = supabase.sign_in(email, password)
            if user:
                session["user"] = {"id": user.id, "email": user.email}
                return redirect(url_for("chat"))
            else:
                flash("Invalid email or password.", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        if not email or not password or not confirm_password:
            flash("Please fill out all fields.", "warning")
            return render_template("register.html")
        if password != confirm_password:
            flash("Passwords do not match.", "warning")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "warning")
            return render_template("register.html")
        try:
            user = supabase.sign_up(email, password)
            if user:
                flash("Your account has been created successfully. You can now log in.", "success")
                return redirect(url_for("login"))
            else:
                flash("Could not create account.", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
    return render_template("register.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect(url_for("login"))
    user = session["user"]
    chat_history = ChatHistory(user["id"])
    if request.method == "POST":
        message_text = request.form.get("message", "").strip()
        if message_text:
            timestamp = datetime.now().isoformat()
            chat_history.add_message("user", message_text, timestamp)
            response = openai_handler.process_message(user["id"], message_text)
            timestamp = datetime.now().isoformat()
            chat_history.add_message("assistant", response, timestamp)
    messages = chat_history.get_messages()
    return render_template("chat.html", user=user, messages=messages)

from flask import jsonify

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/api/chat", methods=["POST"])
def api_chat():
    if "user" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user = session["user"]
    data = request.get_json()
    message_text = data.get("message", "").strip() if data else ""
    if not message_text:
        return jsonify({"error": "Empty message"}), 400
    chat_history = ChatHistory(user["id"])
    timestamp = datetime.now().isoformat()
    chat_history.add_message("user", message_text, timestamp)
    response = openai_handler.process_message(user["id"], message_text)
    timestamp = datetime.now().isoformat()
    chat_history.add_message("assistant", response, timestamp)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
