from flask import Flask
from flask_mysqldb import MySQL
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import jwt
import time
from datetime import datetime, timedelta
import random
import string

app = Flask(__name__)
#Local connection
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'my1T@dmin123'
# app.config['MYSQL_DB'] = 'studentsattendance'
#End local connection

#AWS connection
app.config['MYSQL_HOST'] = 'studentsattendance.chctecotmcfw.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'My1tadmin123'
app.config['MYSQL_DB'] = 'studentsattendance'
#End local connection

# A secret key to be used to encode the JWT token
app.config['SECRET_KEY'] = 'mysecretkey'

# Define a decorator to check for a valid token
def token_required(func):
    def wrapper(*args, **kwargs):
        token = None
        # Check if the Authorization header is present and contains a valid token
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
            try:
                # Decode the token using the secret key
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
                # Pass the user_id as an argument to the function
                return func(data['user_id'], *args, **kwargs)
            except:
                # Return an error message if the token is invalid
                return jsonify({'message': 'Invalid token'}), 401
        else:
            # Return an error message if the Authorization header is missing
            return jsonify({'message': 'Authorization header is missing'}), 401
    return wrapper




@app.route('/get_token', methods=['GET'])
def get_token():
    # Define the payload of the JWT token
    payload = {
        'user': 'app',
        'scope': 'attend',
        'exp': datetime.utcnow() + timedelta(minutes=30)
    }

    # Generate the JWT token using the secret key
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

    # Return the token as a JSON response
    return jsonify({'token': token})


# function to authenticate user with username and password
def authenticate_user(username, password):
    cur = mysql.connection.cursor()
    # create a cursor object to execute SQL queries
    # execute the SQL query to retrieve user information
    query = "SELECT * FROM users WHERE username = %s AND encrypted_password = %s"
    mypass = jwt.encode({'password': password}, 'my-secret-key', algorithm='HS256')
    cur.execute(query, (username, mypass))
    # fetch the first row of the query result
    row = cur.fetchone()
    if row:
        return True
    else:
        return False



@app.route('/login', methods=['POST'])
def login():
    # get the username and password from the request body
    username = request.json.get('username')
    password = request.json.get('password')
    expires = datetime.utcnow() + timedelta(minutes=30)
    # authenticate the user with the given username and password
    if authenticate_user(username, password):
        # generate a JWT token with the username as the payload
        token = jwt.encode({'username': username}, 'my-secret-key', algorithm='HS256')
        # return the token as a JSON response
        return jsonify({'username':username, 'expires': expires, 'token': token})
    else:
        # if authentication fails, return a 401 Unauthorized response
        return jsonify({'message': 'Invalid username or password'}), 401




# API endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    # Read fields from the JSON payload
    username = request.json.get('username')
    email = request.json.get('email')
    encrypted_password = request.json.get('encrypted_password')

    # Validate required fields
    if not username or not email or not encrypted_password:
        return jsonify({'error': 'Missing required fields'}), 400

    cur = mysql.connection.cursor()
   
       # Insert new user into the database
    query = "INSERT INTO users (username, email, encrypted_password) VALUES (%s, %s, %s)" 
    encrypass = jwt.encode({'password': encrypted_password}, 'my-secret-key', algorithm='HS256')
    values = (username, email, encrypass)
    cur.execute(query, values)
    mysql.connection.commit()
    # Return success message
    return jsonify({'message': 'User created successfully'}), 201




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
    token = request.headers.get('Authorization')
    if token:
        try:
            # decode the token and get the username from the payload
            payload = jwt.decode(token, 'my-secret-key', algorithms=['HS256'])
            cur = mysql.connection.cursor()
            # Fetch student data from the database
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
        except jwt.InvalidTokenError:
            # if the token is invalid, return a 401 Unauthorized response
            return jsonify({'message': 'Invalid token'}), 401
    else:
        # if no token is provided, return a 401 Unauthorized response
        return jsonify({'message': 'Token is missing'}), 401




# Get student data enrolled in each module. This returns module and list of students
@app.route('/module/<int:module_id>', methods=['GET'])
def get_module_info(module_id):
    token = request.headers.get('Authorization')
    if token:
        try:
            # decode the token and get the username from the payload
            payload = jwt.decode(token, 'my-secret-key', algorithms=['HS256'])
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
        except jwt.InvalidTokenError:
                # if the token is invalid, return a 401 Unauthorized response
                return jsonify({'message': 'Invalid token'}), 401
    else:
            # if no token is provided, return a 401 Unauthorized response
            return jsonify({'message': 'Token is missing'}), 401

# Get student data enrolled in each module. This returns module and list of students
@app.route('/modulebytutor/<int:tutor_id>', methods=['GET'])
def get_modulebytutor(tutor_id):
    token = request.headers.get('Authorization')
    if token:
        try:
            # decode the token and get the username from the payload
            payload = jwt.decode(token, 'my-secret-key', algorithms=['HS256'])
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

            tutor_query = "SELECT * FROM tutor WHERE tutorid = %s"
            cur.execute(tutor_query, (tutor_id,))
            tutor_row = cur.fetchone()
            cur.close()
            tutor_dict = {
                "tutorId": tutor_row[0],
                "tutorName": tutor_row[1]
            }
            
            tutor_dict["Modules"] = module_list
            return jsonify(tutor_dict)
        except jwt.InvalidTokenError:
                        # if the token is invalid, return a 401 Unauthorized response
            return jsonify({'message': 'Invalid token'}), 401
    else:
                    # if no token is provided, return a 401 Unauthorized response
                    return jsonify({'message': 'Token is missing'}), 401    

#Restrict lessons data to current semester
@app.route('/lessonBySemester/<int:inprogress>', methods=['GET'])
def get_coursesByStatus(inprogress):
    token = request.headers.get('Authorization')
    if token:
        try:
            # decode the token and get the username from the payload
            payload = jwt.decode(token, 'my-secret-key', algorithms=['HS256']) 
            cur = mysql.connection.cursor()
            cur.execute("SELECT * from course where semester = %s", (inprogress,))
            rows = cur.fetchall()
            if not rows:
                return jsonify({'message': 'No record found'}), 404
            else:
                courses = []
                for row in rows:
                    course = {
                    'course_code': row[0],
                    'course_title': row[1],
                    'course_description': row[2],
                    'course_level': row[3],
                    'course_credit': row[4],
                    'semester': row[5]
                    }
                    courses.append(course)
                return {'courses': courses}, 200
        except jwt.InvalidTokenError:
                # if the token is invalid, return a 401 Unauthorized response
                return jsonify({'message': 'Invalid token'}), 401
    else:
            # if no token is provided, return a 401 Unauthorized response
            return jsonify({'message': 'Token is missing'}), 401

#API for bulk attendance upload
@app.route('/bulk_attendance_upload', methods=['POST'])
def bulk_attendance_upload():
    try:
        # Get the JSON data from the request
        data = request.json

        # Get a cursor
        cursor = mysql.connection.cursor()

        # Insert the new timetable event
        cursor.execute("""
            INSERT INTO timetable_event
            (timetable_event_day, timetable_event_description, timetable_event_timestart,
            timetable_event_duration, timetable_event_room, module_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['timetable_event_day'], data['timetable_event_description'],
              data['timetable_event_timestart'], data['timetable_event_duration'],
              data['timetable_event_room'], data['module_id']))
        timetable_event_id = cursor.lastrowid

        # Insert the attendance records
        for attendance_data in data['attendance']:
            cursor.execute("""
                INSERT INTO attendance
                (attendance_date, timetable_event_id, student_id, attendance_code)
                VALUES (%s, %s, %s, %s)
            """, (attendance_data['attendance_date'], timetable_event_id,
                  attendance_data['student_id'], attendance_data['attendance_code']))
        # Commit the changes and close the cursor
        # Check if attendance code is valid
        attendance_code = attendance_data['attendance_code']
        if attendance_code not in ['A', 'O', 'P', 'N', 'C']:
                return jsonify({'message': 'Invalid attendance code'}), 400
        mysql.connection.commit()
        cursor.close()

        # Return a success response
        return {'message': 'Bulk attendance upload successful.'}, 200
    except Exception as e:
        # If there was an error, rollback the transaction and close the cursor
        mysql.connection.rollback()
        cursor.close()
        # Return an error response
        return {'message': 'Bulk attendance upload failed.', 'error': str(e)}, 500



# Endpoint to update attendance record
@app.route('/attendance/<int:attendance_id>', methods=['PUT'])
def update_attendance(attendance_id):
    data = request.get_json()
    token = request.headers.get('Authorization')
    if token:
            try:
                # decode the token and get the username from the payload
                payload = jwt.decode(token, 'my-secret-key', algorithms=['HS256'])
            # Update attendance record in attendance table
                cur = mysql.connection.cursor()
                sql = "UPDATE attendance SET attendance_code = %s WHERE attendance_id = %s"
                val = (data['attendance_code'], attendance_id)
                attendance_code = data['attendance_code']
                #we still need to ensure that only the accepted codes are passed
                if attendance_code not in ['A', 'O', 'P', 'N', 'C']:
                            return jsonify({'message': 'Invalid attendance code'}), 400
                cur.execute(sql, val)
                mysql.connection.commit()
                return jsonify({'message': 'Attendance record updated successfully'})

            except jwt.InvalidTokenError:
                            # if the token is invalid, return a 401 Unauthorized response
                    return jsonify({'message': 'Invalid token'}), 401
    else:
                        # if no token is provided, return a 401 Unauthorized response
            return jsonify({'message': 'Token is missing'}), 401



# Api for adding students
@app.route('/addstudent', methods=['POST'])
def add_student():
    data = request.get_json()
    token = request.headers.get('Authorization')
    if token:
        try:
            # decode the token and get the username from the payload
            payload = jwt.decode(token, 'my-secret-key', algorithms=['HS256']) 
            # Insert student record into students table
            cur = mysql.connection.cursor()
            sql = "INSERT INTO student (student_forename, student_surname, student_email, student_category) VALUES (%s, %s, %s, %s)"
            val = (data['student_forename'], data['student_surname'], data['student_email'], data['student_category'])
            cur.execute(sql, val)
            mysql.connection.commit()

            # Get the auto-generated student_id value
            student_id = cur.lastrowid

            # Insert address record into address table with student_id foreign key
            cur = mysql.connection.cursor()
            sql = "INSERT INTO address (address_number, address_firstline, address_secondline, address_town, address_postcode, address_country, student_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (data['address_number'], data['address_firstline'], data['address_secondline'], data['address_town'], data['address_postcode'], data['address_country'], student_id)
            cur.execute(sql, val)
            mysql.connection.commit()
            return jsonify({'message': 'Student record added successfully'})
        except jwt.InvalidTokenError:
                        # if the token is invalid, return a 401 Unauthorized response
                return jsonify({'message': 'Invalid token'}), 401
    else:
                    # if no token is provided, return a 401 Unauthorized response
        return jsonify({'message': 'Token is missing'}), 401          


# Define API route for updating a student by ID
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
 cur = mysql.connection.cursor()
 student_forename = request.json['student_forename']
 student_surname = request.json['student_surname']
 email = request.json['email']
 student_category = request.json['student_category']
 cur.execute("UPDATE student SET student_forename=%s, student_surname=%s, student_email=%s, student_category=%s WHERE student_id=%s", (student_forename, student_surname, email, student_category, id))
 mysql.connection.commit()
 cur.close()
 return jsonify({'message': 'Student updated successfully'})

# Define API route for deleting a student by ID
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_tutor(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student WHERE student_id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Student deleted successfully'})

# Define API route for updating a student with optional values
@app.route('/students/<int:id>', methods=['PATCH'])
def patch_tutor(id):
    cur = mysql.connection.cursor()
    data = request.get_json()
    student_forename = data.get('student_forename')
    student_surname = data.get('student_surname')
    student_category = data.get('student_category')
    student_email = data.get('student_email')
   
    updates = []
    if student_forename:
        updates.append("student_forename = %s")
    if student_surname:
        updates.append("student_surname = %s")
    if student_category:
        updates.append("student_category = %s")
    if student_email:
        updates.append("email = %s")

    query = "UPDATE student SET " + ", ".join(updates) + " WHERE student_id = %s"
    values = []
    if student_forename:
        values.append(student_forename)
    if student_surname:
        values.append(student_surname)
    if student_category:
        values.append(student_category)
    if student_email:
        values.append(student_email)
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

# lessons fetched to only those which have occurred in the past orare in progress
@app.route('/lessonByStatus/<int:inprogress>', methods=['GET'])
def get_lessonByStatus(inprogress):
    cur = mysql.connection.cursor()
    cur.execute("SELECT course_code, course_title, course_description, course_level, CASE WHEN in_progress =1 THEN TRUE ELSE FALSE END AS Inprogress, semester  FROM course  where in_progress=%s", (inprogress,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
        modules = []
        for row in rows:
            module = {
                'course_code': row[0],
                'course_title': row[1],
                'course_description': row[2],
                'course_level': row[3],
                'Inprogress':bool(row[4]),
                'semester': row[5],
            }
            modules.append(module)
        return {'lessons': modules}, 200


# lessons fetched to only current semester
@app.route('/lessonBySemester/<int:semester>', methods=['GET'])
def get_lessonBySemester(semester):
    cur = mysql.connection.cursor()
    cur.execute("SELECT course_code, course_title, course_description, course_level, CASE WHEN in_progress =1 THEN TRUE ELSE FALSE END AS Inprogress, semester  FROM course  where semester=%s", (semester,))
    rows = cur.fetchall()
    if not rows:
          return jsonify({'message': 'No record found'}), 404
    else:
        modules = []
        for row in rows:
            module = {
                'course_code': row[0],
                'course_title': row[1],
                'course_description': row[2],
                'course_level': row[3],
                'Inprogress':bool(row[4]),
                'semester': row[5],
            }
            modules.append(module)
        return {'lessons': modules}, 200



#View previous attendance date format YYYY-MM-DD
@app.route('/previousattendance', methods=['GET'])
def get_attendance():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    student_id = request.args.get('student_id')
    try:
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD.'}), 400
    cursor = mysql.connection.cursor()
    if student_id:
        cursor.execute("SELECT attendance_id, attendance_date, timetable_event_id, attendance.student_id, attendance_code, student_forename, student_surname, student_email, student_category FROM attendance JOIN student ON attendance.student_id = student.student_id WHERE attendance_date BETWEEN %s AND %s AND attendance.student_id = %s", (start_date_obj, end_date_obj, student_id))
    else:
        cursor.execute("SELECT attendance_id, attendance_date, timetable_event_id, attendance.student_id, attendance_code, student_forename, student_surname, student_email, student_category FROM attendance JOIN student ON attendance.student_id = student.student_id WHERE attendance_date BETWEEN %s AND %s", (start_date_obj, end_date_obj))
    result = cursor.fetchall()
    if not result:
          return jsonify({'message': 'No record found'}), 404
    else:
        atts = []
        for row in result:
            att = {
                'attendance_id': row[0],
                'attendance_date': row[1],
                'timetable_event_id': row[2],
                'student_id': row[3],
                'attendance_code':row[4],
                'student_forename':row[5],
                'student_surname':row[6],
                'student_email':row[7]
            }
            atts.append(att)
    cursor.close()

    return {'previous_attendance': atts}, 200



# Endpoint to create check-in code record
@app.route('/createcheckin', methods=['POST'])
def add_checkin():
    data = request.get_json()
    cur = mysql.connection.cursor()
    # Generate a random six-letter code
    code = '-'.join([''.join(random.choices(string.ascii_uppercase, k=2)) for i in range(3)])

    # Get the current date and time
    course_date = datetime.now()

    # Insert check-in code record into check_in_code table
    sql = "INSERT INTO check_in_code (course_code, code, course_date) VALUES (%s, %s, %s)"
    val = (data['course_code'], code, course_date)
    cur.execute(sql, val)
    mysql.connection.commit()

    return jsonify({'message':  "Checkin code created", 'Check-in Code': code }), 200



# Endpoint for self check-in
@app.route('/self_checkin', methods=['POST'])
def add_attendance():
    data = request.get_json()

    # Check if the course_code and code exist in the check_in_code table
    cur = mysql.connection.cursor()
    curr = mysql.connection.cursor()
    sql = "SELECT * FROM check_in_code WHERE course_code = %s AND code = %s"
    val = (data['course_code'], data['code'])
    cur.execute(sql, val)
    check_in_code = cur.fetchone()
    attendance_code = data['attendance_code']
    if attendance_code not in ['P']:
        return jsonify({'error': 'Invalid attendance code'}), 400

    if check_in_code is None:
        return jsonify({'error':  "Invalid course code or check-in code"}), 400
    # sql ="SELECT module_id from module WHERE course_code = %s"
    # val = (data['course_code'])
    # cur.execute(sql, val)
    # module_id = cur.fetchone()

    # Get the student_id from the request body
    student_id = data['student_id']

    # Get the current date and time
    attendance_date = datetime.now()

    cur.execute("""
            INSERT INTO timetable_event
            (timetable_event_day, timetable_event_description, timetable_event_timestart,
            timetable_event_duration, timetable_event_room, module_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data['timetable_event_day'], data['timetable_event_description'],
              data['timetable_event_timestart'], data['timetable_event_duration'],
              data['timetable_event_room'], data['module_id']))
    timetable_event_id = cur.lastrowid



    # # Insert record into timetable_event table
    # sql = "INSERT INTO timetable_event (timetable_event_day, timetable_event_description, timetable_event_timestart, timetable_event_duration, timetable_event_room, module_id) VALUES (%s, %s, %s, %s, %s, %s)"
    # val = (data['timetable_event_day'], data['timetable_event_description'], data['timetable_event_timestart'], data['timetable_event_duration'], data['timetable_event_room'], module_id)
    # cur.execute(sql, val)
    # mysql.connection.commit()
    # timetable_event_id = cur.lastrowid
    # Insert record into attendance table
    sql = "INSERT INTO attendance (attendance_date, timetable_event_id, student_id, attendance_code) VALUES (%s, %s, %s, %s)"
    val = (attendance_date, timetable_event_id, student_id, attendance_code)
    cur.execute(sql, val)
    mysql.connection.commit()

    return jsonify({'message':  "Check in was succesful, you've been marked present"}), 200










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

