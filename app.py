from flask import Flask, request, render_template, jsonify
import os
from statistics import mean, stdev

app = Flask(__name__)

# Store students in memory (for demo purposes)
students = []

def validate_student_input(name, age, gender, student_id, marks):
    """
    Validate student input
    """
    errors = []
    
    if not name or not name.strip():
        errors.append("Name cannot be empty!")
    
    try:
        age = int(age)
        if age < 5 or age > 100:
            errors.append("Age must be between 5 and 100!")
    except ValueError:
        errors.append("Age must be a valid number!")
    
    if gender not in ["Male", "Female", "Other"]:
        errors.append("Please select a valid gender!")
    
    if not student_id or not student_id.strip():
        errors.append("Student ID cannot be empty!")
    
    try:
        marks = float(marks)
        if marks < 0 or marks > 100:
            errors.append("Marks must be between 0 and 100!")
    except ValueError:
        errors.append("Marks must be a valid number!")
    
    return errors, age, marks

@app.route("/")
def home():
    return render_template('index.html', total_students=len(students))

@app.route('/add_student', methods=['POST'])
def add_student():
    try:
        data = request.form
        name = data.get('name', '').strip()
        age = data.get('age', '')
        gender = data.get('gender', '')
        student_id = data.get('student_id', '').strip()
        marks = data.get('marks', '')
        
        # Validate input
        errors, age, marks = validate_student_input(name, age, gender, student_id, marks)
        
        if errors:
            return jsonify({'success': False, 'errors': errors}), 400
        
        # Add student to list
        student_data = {
            "Name": name,
            "Age": int(age),
            "Gender": gender,
            "Student ID": student_id,
            "Marks": float(marks)
        }
        students.append(student_data)
        
        return jsonify({
            'success': True, 
            'message': 'Student information added successfully!',
            'total_students': len(students)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'errors': [str(e)]}), 500

@app.route('/get_students', methods=['GET'])
def get_students():
    """Get all students"""
    try:
        if not students:
            return jsonify({'success': True, 'students': [], 'count': 0}), 200
        
        ages = [s['Age'] for s in students]
        marks = [s['Marks'] for s in students]
        
        stats = {
            'total': len(students),
            'avg_age': round(mean(ages), 2),
            'avg_marks': round(mean(marks), 2),
            'highest_marks': max(marks),
            'lowest_marks': min(marks)
        }
        
        return jsonify({
            'success': True,
            'students': students,
            'count': len(students),
            'stats': stats
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_csv', methods=['GET'])
def download_csv():
    """Download student data as CSV"""
    try:
        if not students:
            return jsonify({'success': False, 'error': 'No students to download'}), 400
        
        csv_file = 'student_data.csv'
        with open(csv_file, 'w') as f:
            # Write header
            f.write('Name,Age,Gender,Student ID,Marks\n')
            # Write data
            for student in students:
                f.write(f"{student['Name']},{student['Age']},{student['Gender']},{student['Student ID']},{student['Marks']}\n")
        
        return jsonify({
            'success': True,
            'message': f'CSV file created: {csv_file}'
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/clear_all', methods=['POST'])
def clear_all():
    """Clear all student records"""
    global students
    students = []
    return jsonify({'success': True, 'message': 'All records cleared!'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
