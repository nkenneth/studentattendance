from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
# conn = sqlite3.connect('UniNorthwest.db')
# c = conn.cursor()

# # create the students table with the specified columns
# c.execute('''CREATE TABLE students
#              (Id INTEGER PRIMARY KEY,
#               name TEXT,
#               gender id,
#               email TEXT,
#               phone TEXT,
#               creationDate DATETIME)''')

# # commit the changes and close the connection
# conn.commit()
# conn.close()


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'my1T@dmin123'
app.config['MYSQL_DB'] = 'studentsattendance'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UniNorthwest.db'
#db = SQLAlchemy(app)

# class students(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))
#     gender = db.Column(db.Integer)
#     email = db.Column(db.String(10))

@app.route('/allstudents', methods=['GET'])
def get_all_students():
    students = students.query.all()
    results = []
    for student in students:
        student_data = {}
        student_data['id'] = student.id
        student_data['name'] = student.name
        student_data['gender'] = student.gender
        student_data['email'] = student.email
        results.append(student_data)
    return jsonify(results)



# API for getting students 
mysql = MySQL(app)
@app.route('/students')
def get_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT student.student_id, student.student_forename, student.student_surname, student.student_email, student.student_category, student.CreationDate, CONCAT(address.address_number, ', ', address.address_firstline, ' ', address.address_town, ' ', address.address_postcode, ' ', address.address_country) FROM student INNER JOIN address ON student.student_id = address.student_id;")
    rows = cur.fetchall()
    students = []
    for row in rows:
        student = {
            'student_id': row[0],
            'student_forename': row[1],
            'student_surname': row[2],
            'student_email': row[3],
            'student_category': row[4],
            'creation_date': row[5],
            'student_address': row[6],

        }
        students.append(student)
    return {'students': students}, 200



# Get student data enrolled in each module returning students per modules
@app.route('/modulestudents/<int:module_id>', methods=['GET'])
def get_modulestudents(module_id):
    cur = mysql.connection.cursor()
    cur.execute("select module.module_id, module.module_title, module.module_description, module.module_level, student.student_forename, student.student_surname from module inner join enrolment on enrolment.module_id = module.module_id inner join student on student.student_id = enrolment.student_id where module.module_id=%s", (module_id,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
        modules = []
        for row in rows:
            module = {
                'module_id': row[0],
                'module_title': row[1],
                'module_description': row[2],
                'module_level': row[3],
                'student_forename' : row[4],
                'student_surname' : row[5]
            }
            modules.append(module)
        return {'modules': modules}, 200

# Get student data enrolled in each module. This returns module and list of students
@app.route('/module/<int:module_id>', methods=['GET'])
def get_module_info(module_id):
    cur = mysql.connection.cursor()
    module_query = "SELECT * FROM module WHERE module_id = %s"
    cur.execute(module_query, (module_id,))
    module_row = cur.fetchone()
    if not module_row:
        return jsonify({'message': 'No record found'}), 404
    else:
        module_dict = {
        "module_id": module_row[0],
        "module_title": module_row[1],
        "module_description": module_row[2],
        "module_level": module_row[3]
        }
    student_query = "SELECT student_forename, student_surname FROM enrolment INNER JOIN student ON enrolment.student_id = student.student_id WHERE enrolment.module_id = %s"
    cur.execute(student_query, (module_id,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
     student_list = []
    for row in rows:
        student_dict = {
            "student_forename": row[0],
            "student_surname": row[1]
        }
        student_list.append(student_dict)
    module_dict["students"] = student_list
    return jsonify(module_dict)

# Get student data enrolled in each module. This returns module and list of students
@app.route('/modulebytutor/<int:tutor_id>', methods=['GET'])
def get_modulebytutor(tutor_id):
    cur = mysql.connection.cursor()
    #module_query = "SELECT * FROM module WHERE tutor_id = %s"
    module_query = " select module.module_id, module.module_title, module.module_description, module.module_level, module.module_credits, module.course_code from module inner join tutor on module.tutorId = tutor.tutorId where module.tutorId= %s"
    cur.execute(module_query, (tutor_id,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
        module_list = []
    for row in rows:
        module_dict = {
            "module_id": row[0],
            "module_title": row[1],
            "module_description": row[2],
            "module_level": row[3], 
            "module_credits": row[4], 
            "course_code": row[5]
        }
        module_list.append(module_dict)

    tutor_query = "SELECT * FROM TUTOR WHERE tutorid = %s"
    cur.execute(tutor_query, (tutor_id,))
    tutor_row = cur.fetchone()
    cur.close()
    tutor_dict = {
        "tutorId": tutor_row[0],
        "tutorName": tutor_row[1]
    }
    
    tutor_dict["Modules"] = module_list
    return jsonify(tutor_dict)









# Api for adding students
from flask import request
@app.route('/addstudent', methods=['POST'])
def add_student():
    student_name = request.json['student_name']
    gender = request.json['gender']
    email = request.json['email']
    phone = request.json['phone']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students (name, gender, email, phone) VALUES (%s, %s, %s, %s)", (student_name, gender, email, phone))
    mysql.connection.commit()
    return {'message': 'Student added successfully'}


# Define API route for updating a student by ID
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
 cur = mysql.connection.cursor()
 name = request.json['name']
 gender = request.json['gender']
 email = request.json['email']
 phone = request.json['phone']
 cur.execute("UPDATE students SET name=%s, gender=%s, email=%s, phone=%s WHERE id=%s", (name, gender, email, phone, id))
 mysql.connection.commit()
 cur.close()
 return jsonify({'message': 'Student updated successfully'})

# Define API route for deleting a student by ID
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_tutor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student deleted successfully'})

# Define API route for updating a student with optional values
@app.route('/students/<int:id>', methods=['PATCH'])
def patch_tutor(id):
    cur = mysql.connection.cursor()
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    email = data.get('email')
    phone = data.get('phone')
    updates = []
    if name:
        updates.append("name = %s")
    if gender:
        updates.append("gender = %s")
    if email:
        updates.append("email = %s")
    if phone:
        updates.append("phone = %s")
    query = "UPDATE students SET " + ", ".join(updates) + " WHERE id = %s"
    values = []
    if name:
        values.append(name)
    if gender:
        values.append(gender)
    if email:
        values.append(email)
    if phone:
        values.append(phone)
    values.append(id)
    cur.execute(query, tuple(values))
    num_rows_affected = cur.rowcount
    mysql.connection.commit()
    cur.close()
    if num_rows_affected == 0:
        return jsonify({'message': 'No record was updated'}), 404
    else:
        return jsonify({'message': 'Student updated successfully'}), 200

# Get tutors
@app.route('/tutor')
def get_tutors():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM tutor")
    rows = cur.fetchall()
    tutors = []
    for row in rows:
        tutor = {
            'Id': row[0],
            'Name': row[1],
            'CreationDate': row[2]
        }
        tutors.append(tutor)
    return {'tutors': tutors}, 200

# Get tutors by Module
@app.route('/tutorbymoduleId/<int:tutor_id>', methods=['GET'])
def get_tutorsbyModule(tutor_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT modules.Id, modules.Modulename, tutor.Name, modules.TutorId FROM modules INNER JOIN tutor ON modules.TutorId = tutor.Id where modules.TutorId=%s", (tutor_id,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
        modules = []
        for row in rows:
            module = {
                'Id': row[0],
                'ModuleName': row[1],
                'TutorName': row[2],
                'TutorId': row[3]
            }
            modules.append(module)
        return {'modules': modules}, 200

# Get lessons  by when it occured
@app.route('/lessonByStatus/<int:inprogress>', methods=['GET'])
def get_lessonByStatus(inprogress):
    cur = mysql.connection.cursor()
    cur.execute("SELECT modules.Id, modules.Modulename, semester.semesteryear, semester.semesterName, CASE WHEN inprogress =1 THEN TRUE ELSE FALSE END AS isActive  FROM modules INNER JOIN semester ON modules.semesterid = semester.Id where semester.inprogress=%s", (inprogress,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
        modules = []
        for row in rows:
            module = {
                'Id': row[0],
                'ModuleName': row[1],
                'SemesterYear': row[2],
                'SemesterName': row[3],
                'Inprogress':bool(row[4])
            }
            modules.append(module)
        return {'modules': modules}, 200

#Bulk insert to student attendance table 
@app.route('/studentattendance/bulk', methods=['POST'])
def bulk_insert_studentattendance():
    if request.method == 'POST':
        attendance = request.json
        if not attendance:
            return jsonify({'message': 'No data provided'}), 400
        else:
            cur = mysql.connection.cursor()
            values = []
            for att in attendance:
                student_id = att.get('StudentId')
                module_id = att.get('ModuleId')
                is_checked_in = att.get('IsCheckedIn')
                values.append((student_id, module_id, is_checked_in))
            try:
                cur.executemany("INSERT INTO studentattendance (StudentId, ModuleId, IsCheckedIn) VALUES (%s, %s, %s)", values)
                mysql.connection.commit()
            except:
                mysql.connection.rollback()
                return jsonify({'message': 'Error inserting data'}), 500
            cur.close()
            return jsonify({'message': f"{len(attendance)} attendance records inserted"}), 201














# mysql = MySQL(app)
# @app.route('/modules')
# def get_modules():
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM tbl_modules")
#     rows = cur.fetchall()
#     modules = []
#     for row in rows:
#         module = {
#             'id': row[0],
#             'module_name': row[1],
#             'tutor': row[2]
#         }
#         modules.append(module)
#     return {'modules': modules}





# from flask import request
# @app.route('/modules', methods=['POST'])
# def add_module():
#     module_name = request.json['module_name']
#     tutor = request.json['tutor']
#     cur = mysql.connection.cursor()
#     cur.execute("INSERT INTO tbl_modules (module_name, tutor) VALUES (%s, %s)", (module_name, tutor))
#     mysql.connection.commit()
#     return {'message': 'Module added successfully'}

# # This is the api that fecthes module based on assigned tutor
# @app.route('/modules/<tutor>')
# def get_modules_by_tutor(tutor):
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT * FROM tbl_modules WHERE tutor=%s", (tutor,))
#     rows = cur.fetchall()
#     modules = []
#     for row in rows:
#         module = {
#             'id': row[0],
#             'module_name': row[1],
#             'tutor': row[2]
#         }
#         modules.append(module)
#     return {'modules': modules}

