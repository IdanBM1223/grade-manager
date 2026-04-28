from flask import Flask, jsonify , request
import sqlite3




class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

students = [
    Student("Idan", 90),
    Student("Non", 56),
    Student("buli", 95)
]
result = []

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            grade REAL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return "Hello World!"


@app.route("/students")
def get_students():
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([{"id": row[0], "name": row[1], "grade": row[2]} for row in rows])
    # result = []
    # for stud in students:
    #     result.append({"name": stud.name, "grade": stud.grade})
    # return jsonify(result)


@app.route("/stats")
def get_stats():
    grade = [stud.grade for stud in students]
    return jsonify({
        "average": sum(grade)/len(grade),
        "highest": max(grade),
        "lowest": min(grade)
     })



@app.route("/students", methods = ["POST"])
def add_student():
    data = request.get_json(silent=True)
    if not data or "name" not in data or "grade" not in data:
        return jsonify({"message": "missing name or grade"}), 400
 
    name = data["name"]
    new_grade= data["grade"]
    conn = sqlite3.connect('students.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO students (name, grade) VALUES (?, ?)", (name, new_grade)
    )
    conn.commit()
    conn.close()
    return jsonify({"message": "Student added!"})


@app.route("/students/<name>", methods = ["DELETE"])
def delete_student(name):
   conn = sqlite3.connect('students.db')
   cursor = conn.cursor()
   cursor.execute("DELETE FROM students Where name = ?", (name,))
   conn.commit()
   if cursor.rowcount == 0 :
        conn.close()
        return jsonify({"message": "Student not found!"}), 404
   conn.close()
   return jsonify({"message": "Student deleted!"})



@app.route("/students/<name>", methods =["PUT"])
def update(name):
    data = request.get_json(silent=True)
    if not data or "grade" not in data:
         return jsonify({"message": "missing name or grade"}), 400
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE students SET grade = ? WHERE name = ?", (data["grade"], name))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Student not found!"}), 404
    conn.close()
    return jsonify({"message": "Student updated!"}), 200








if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)