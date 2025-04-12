import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from supabase import create_client, Client

app = Flask(__name__)

app.secret_key = 's0m3_th1ng_r@nd0m_4nd_s3cur3'

# Supabase config
SUPABASE_URL = "https://diufwzticauqwknuqadn.supabase.co"  # Replace with your Supabase URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpdWZ3enRpY2F1cXdrbnVxYWRuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ0NDcwODcsImV4cCI6MjA2MDAyMzA4N30.VdZ5iadnuFBBpp2w1zJCrRA3jQd5TSx9ldZbWey4e9Q"  # Replace with your Supabase Key

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# File upload config
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    # Get all application entries
    applications = supabase.table("applications").select("*").order("date_submitted", desc=True).execute().data

    # Get counts by status
    counts = supabase.table("applications").select("status").execute().data
    status_counts = {
        'total': len(counts),
        'Pending': sum(1 for x in counts if x['status'] == 'Pending'),
        'Approved': sum(1 for x in counts if x['status'] == 'Approved'),
        'Rejected': sum(1 for x in counts if x['status'] == 'Rejected')
    }

    return render_template('admin.html', applications=applications, stats=status_counts)

@app.route('/apply_page')
def apply_page():
    return render_template('apply.html')

@app.route('/organization_page')
def organization_page():
    return render_template('organization.html')

@app.route("/approve/<int:applicant_id>", methods=["POST"])
def approve_applicant(applicant_id):
    supabase.table("applications").update({"status": "Approved"}).eq("id", applicant_id).execute()
    flash('Applicant Approved successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route("/reject/<int:applicant_id>", methods=["POST"])
def reject_applicant(applicant_id):
    supabase.table("applications").update({"status": "Rejected"}).eq("id", applicant_id).execute()
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

        # Get the file binary content
        image_binary = file.read()

        # Initialize Supabase storage and access the 'id' bucket
       

        try:
        #     # Upload the file to Supabase storage bucket
            file_path = f"applications/{filename}"

        #     # Upload directly using image_binary
            storage_response = supabase.storage.from_("id").upload(file_path, image_binary)
            image_url = f"{SUPABASE_URL}/storage/v1/object/public/id/applications/{filename}"

        #     # Check if the upload was successful
        #     if storage_response.get("error") is None:
                # Save application data to Supabase database
            supabase.table("applications").insert({
                    "last_name": last_name,
                    "first_name": first_name,
                    "age": age,
                    "email": email,
                    "phone_number": phone_number,
                    "birthdate": birthdate,
                    "sex": sex,
                    "civil_status": civil_status,
                    "valid_id": image_url
                }).execute()
            
            flash('Applicant Submitted successfully!', 'success')
            # else:
            #     flash(f"File upload failed: {storage_response['error']['message']}", 'danger')

        except Exception as e:
            flash(f"Error: {str(e)}", 'danger')


        return render_template('apply.html')
                
@app.route('/delete_applicant/<int:applicant_id>', methods=['POST'])
def delete_applicant(applicant_id):
    supabase.table("applications").delete().eq("id", applicant_id).execute()
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
        supabase.table("applications").update({
            "last_name": last_name,
            "first_name": first_name,
            "age": age,
            "email": email,
            "phone_number": phone_number,
            "birthdate": birthdate,
            "sex": sex,
            "civil_status": civil_status,
            "valid_id": filename
        }).eq("id", applicant_id).execute()
    else:
        # No ID update
        supabase.table("applications").update({
            "last_name": last_name,
            "first_name": first_name,
            "age": age,
            "email": email,
            "phone_number": phone_number,
            "birthdate": birthdate,
            "sex": sex,
            "civil_status": civil_status
        }).eq("id", applicant_id).execute()

    flash('Applicant updated successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
