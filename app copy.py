import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 's0m3_th1ng_r@nd0m_4nd_s3cur3'
# MySQL config
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'brgyease_db'

# File upload config
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    cur = mysql.connection.cursor()
    
    # Get all application entries
    cur.execute("SELECT * FROM applications ORDER BY date_submitted DESC")
    applications = cur.fetchall()

    # Get counts by status
    cur.execute("""
        SELECT 
            COUNT(*) AS total,
            SUM(status = 'Pending') AS Pending,
            SUM(status = 'Approved') AS Approved,
            SUM(status = 'Rejected') AS Rejected
        FROM applications
    """)
    counts = cur.fetchone()

    cur.close()

    stats = {
        'total': counts[0],
        'Pending': counts[1],
        'Approved': counts[2],
        'Rejected': counts[3]
    }

    return render_template('admin.html', applications=applications, stats=stats)

@app.route('/apply_page')
def apply_page():
    return render_template('apply.html')

@app.route('/organization_page')
def organization_page():
    return render_template('organization.html')

@app.route("/approve/<int:applicant_id>", methods=["POST"])
def approve_applicant(applicant_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE applications SET status = 'Approved' WHERE id = %s", (applicant_id,))
    mysql.connection.commit()
    cur.close()
    flash('Applicant Approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route("/reject/<int:applicant_id>", methods=["POST"])
def reject_applicant(applicant_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE applications SET status = 'Rejected' WHERE id = %s", (applicant_id,))
    mysql.connection.commit()
    cur.close()
    flash('Applicant Rejected successfully!', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/apply', methods=['POST'])
def apply():
    if request.method == 'POST':
        # Get form fields
        last_name = request.form['lastName']
        first_name = request.form['firstName']
        age = request.form['age']
        email = request.form['email']
        phone_number = request.form['phone']
        birthdate = request.form['birthdate']
        sex = request.form['sex']
        civil_status = request.form['Status']

        # Handle file upload
        file = request.files['idPhoto']
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Save to DB
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO applications (
                last_name, first_name, age, email, phone_number,
                birthdate, sex, civil_status, valid_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (last_name, first_name, age, email, phone_number,
              birthdate, sex, civil_status, filename))
        mysql.connection.commit()
        cur.close()

    flash('Applicant Submitted successfully!', 'success')

    return render_template('apply.html')

@app.route('/delete_applicant/<int:applicant_id>', methods=['POST'])
def delete_applicant(applicant_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM applications WHERE id = %s", (applicant_id,))
    mysql.connection.commit()
    cur.close()
    flash('Applicant Deleted successfully!', 'danger')
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_applicant/<int:applicant_id>', methods=['POST'])
def edit_applicant(applicant_id):
    last_name = request.form['lastName']
    first_name = request.form['firstName']
    age = request.form['age']
    email = request.form['email']
    phone_number = request.form['phone']
    birthdate = request.form['birthdate']
    sex = request.form['sex']
    civil_status = request.form['Status']
    file = request.files['idPhoto']

    # Save updated valid ID only if uploaded
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Update with new ID path
        query = """UPDATE applications SET last_name=%s, first_name=%s, age=%s, email=%s,
                   phone_number=%s, birthdate=%s, sex=%s, civil_status=%s, valid_id=%s
                   WHERE id=%s"""
        values = (last_name, first_name, age, email, phone_number, birthdate, sex, civil_status, filename, applicant_id)
    else:
        # No ID update
        query = """UPDATE applications SET last_name=%s, first_name=%s, age=%s, email=%s,
                   phone_number=%s, birthdate=%s, sex=%s, civil_status=%s
                   WHERE id=%s"""
        values = (last_name, first_name, age, email, phone_number, birthdate, sex, civil_status, applicant_id)

    cursor = mysql.connection.cursor()
    cursor.execute(query, values)
    mysql.connection.commit()
    cursor.close()
    flash('Applicant updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
