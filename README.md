# VISIT ONLINE 
https://brgyease.vercel.app/

# BrgyEase Application Portal

BrgyEase is a simple web-based application system for barangay applicants, featuring a clean admin dashboard and CRUD operations for managing applications.

## 🚀 Features

- 🌐 Public-facing pages:
  - Home page
  - Application form page
  - Organization info page
- 📥 Submit applications with file uploads (valid ID)
- 📊 Admin dashboard:
  - View all applications
  - View application statistics (Pending, Approved, Rejected)
  - Approve, reject, edit, or delete applicants
- ✅ Flash message notifications on all actions
- 🧠 Fully server-rendered
- 📁 Uploaded files saved under `static/uploads`

## 🛠️ Built With

- Python 3
- Flask
- MySQL (via `flask-mysqldb`)
- HTML, CSS, JS

## 🗃️ Database Schema

```sql
CREATE TABLE applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(100),
    first_name VARCHAR(100),
    age INT,
    email VARCHAR(255),
    phone_number VARCHAR(20),
    birthdate DATE,
    sex VARCHAR(10),
    civil_status VARCHAR(20),
    valid_id VARCHAR(255),
    status VARCHAR(20) DEFAULT 'Pending',
    date_submitted TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🧑‍💻 How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/brgyease.git
   cd brgyease
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up MySQL:
   - Create a database named `brgyease_db`
   - Import the table structure (see schema above)

5. Configure `app.py`:
   Update these lines as needed:
   ```python
   app.config['MYSQL_HOST'] = 'localhost'
   app.config['MYSQL_USER'] = 'root'
   app.config['MYSQL_PASSWORD'] = ''
   app.config['MYSQL_DB'] = 'brgyease_db'
   ```

6. Run the app:
   ```bash
   python app.py
   ```

7. Visit:
   ```
   http://127.0.0.1:5000/
   ```

## 📂 Folder Structure

```
brgyease/
│
├── app.py
├── templates/
│   ├── index.html
│   ├── apply.html
│   ├── organization.html
│   └── admin.html
├── static/
│   └── uploads/
├── requirements.txt
└── README.md
```

## 💡 Notes

- Flash messages are used for user feedback and require a `secret_key`, which is already set in `app.py`.
- File uploads are saved to `static/uploads`, make sure this folder exists.
- Page updates use full reloads with Flask routes.

## 📧 Contact

For questions or support, feel free to reach out at [your_email@example.com] or create an issue in this repository.

---

> Made with ❤️ by Dennrick (Ekskie)
```

---

Let me know if you'd like me to include a `requirements.txt` or a sample `.env` configuration too!
