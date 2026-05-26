from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

DATA_FILE = "attendance.txt"
STUDENT_FILE = "students.txt"


@app.route('/')
def home():
    return render_template('index.html')


# ADD STUDENT
@app.route('/add_student', methods=['POST'])
def add_student():

    data = request.json

    roll = data.get('roll')
    name = data.get('name')

    try:

        # Prevent duplicate roll numbers
        if os.path.exists(STUDENT_FILE):

            with open(STUDENT_FILE, 'r') as file:

                for line in file.readlines():

                    existing_roll = line.strip().split(',')[0]

                    if existing_roll == roll:

                        return jsonify({
                            'success': False,
                            'message': 'Roll Number Already Exists'
                        })

        with open(STUDENT_FILE, 'a') as file:

            file.write(f"{roll},{name}\n")

        return jsonify({
            'success': True,
            'message': 'Student Added Successfully'
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'message': str(e)
        })


# GET ALL STUDENTS
@app.route('/get_students')
def get_students():

    students = []

    try:

        if not os.path.exists(STUDENT_FILE):
            return jsonify([])

        with open(STUDENT_FILE, 'r') as file:

            lines = file.readlines()

            for line in lines:

                parts = line.strip().split(',')

                if len(parts) >= 2:

                    students.append({
                        'roll': parts[0],
                        'name': parts[1]
                    })

        return jsonify(students)

    except Exception as e:

        return jsonify({
            'error': str(e)
        })


# SAVE DAILY ATTENDANCE
@app.route('/add_attendance', methods=['POST'])
def add_attendance():

    data = request.json

    attendance_data = data.get('attendance')

    try:

        with open(DATA_FILE, 'a') as file:

            for student in attendance_data:

                file.write(
                    f"{student['roll']} "
                    f"{student['name']} "
                    f"{student['status']}\n"
                )

        return jsonify({
            'success': True,
            'message': 'Attendance Saved Successfully'
        })

    except Exception as e:

        return jsonify({
            'success': False,
            'message': str(e)
        })


# VIEW RECORDS + PERCENTAGE
@app.route('/view_records')
def view_records():

    students = {}

    try:

        # LOAD STUDENTS
        if os.path.exists(STUDENT_FILE):

            with open(STUDENT_FILE, 'r') as file:

                for line in file.readlines():

                    parts = line.strip().split(',')

                    if len(parts) >= 2:

                        roll = parts[0]
                        name = parts[1]

                        students[roll] = {
                            'name': name,
                            'present': 0,
                            'total': 0
                        }

        # LOAD ATTENDANCE
        if os.path.exists(DATA_FILE):

            with open(DATA_FILE, 'r') as file:

                for line in file.readlines():

                    parts = line.strip().split()

                    if len(parts) >= 3:

                        roll = parts[0]
                        status = parts[2]

                        if roll in students:

                            students[roll]['total'] += 1

                            if status == 'P':

                                students[roll]['present'] += 1

        records = []

        for roll, data in students.items():

            percentage = 0

            if data['total'] > 0:

                percentage = (
                    data['present'] / data['total']
                ) * 100

            records.append({

                'roll': roll,

                'name': data['name'],

                'present': data['present'],

                'total': data['total'],

                'percentage': round(percentage, 1)
            })

        return jsonify(records)

    except Exception as e:

        return jsonify({
            'error': str(e)
        })


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
