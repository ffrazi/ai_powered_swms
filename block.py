from flask import Flask, request, jsonify
import sqlite3

app = Flask(_name_)

# Initialize the database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_data TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()  # Call this function to create the database

@app.route("/save_log", methods=["POST"])
def save_log():
    try:
        data = request.json  # Capture JSON payload
        print("Received data:", data)  # Debugging step

        if not data:
            return jsonify({"message": "No data received"}), 400

        log_data = str(data)  # Convert to string if needed

        # Insert into SQLite database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO logs (log_data) VALUES (?)", (log_data,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Log saved successfully!"})

    except Exception as e:
        print("Error:", str(e))  # Debugging step
        return jsonify({"message": f"Error: {str(e)}"}), 500

if _name_ == "_main_":
    app.run(debug=True)