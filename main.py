from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT
        )''')

@app.route("/")
def index():
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form["title"]
    category = request.form["category"]
    print(f"Adding task: {title} ({category})") 
        
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, category, completed) VALUES (?, ?, 0)", (title, category))
        conn.commit()
        
    return redirect("/")

@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()
    return redirect("/")  # This ends the delete_task route.

@app.route("/toggle/<int:task_id>")
def toggle_task(task_id):
    with sqlite3.connect("database.db") as conn:
        cursor = conn.cursor()
        # Toggle completion: 0 becomes 1, 1 becomes 0
        cursor.execute("UPDATE tasks SET completed = NOT completed WHERE id = ?", (task_id,))
        conn.commit()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    print("Flask app is running!")
    app.run(debug=True)

