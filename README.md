📦 Order Management System 

This project is a backend template built using Django Rest Framework with Google OAuth 2.0 authentication. It allows users to authenticate via their Google accounts and perform secure data entry and retrieval through REST API endpoints.

Developed as part of the Ywork.ai backend assignment.

🔧 Features

    🔐 Google OAuth 2.0 Authentication
    Secure user login via Google. Retrieves and stores access and refresh tokens.

    📤 Add Sample Data
    Users can add structured entries (title + description) to the database.

    📥 Retrieve Filtered Data
    Search entries by title via query parameters. API access is protected.

📁 Project Structure

myproject/
├── manage.py
├── myapp/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
├── myproject/
│   ├── settings.py
│   └── urls.py
├── .gitignore
├── README.md
└── client_secret.json (excluded)

⚙️ Setup Instructions
1. Clone the repository

git clone https://github.com/plastic07/myproject.git
cd myproject

2. Create a virtual environment and activate

python3 -m venv venv
source venv/bin/activate

3. Install dependencies

pip install -r requirements.txt

4. Add your Google OAuth credentials

    Go to the Google Cloud Console.

    Create an OAuth 2.0 Client ID.

    Download client_secret.json and place it in the root directory (same level as manage.py).

    Do not commit this file. It is excluded by .gitignore.

5. Apply migrations

python manage.py migrate

6. Start the development server

python manage.py runserver



🔗 API Usage
🔑 Google OAuth2 Authentication

Visit this URL in your browser to trigger OAuth:
[
http://127.0.0.1:8000/oauth2callback/

Or initiate via Postman with your client credentials.

POST /api/data/

Add a new entry (authenticated):

{
  "title": "Sample Entry",
  "description": "This is a test description."
}

GET /api/data/?title=Sample

Fetch entries matching a specific title (authenticated):

GET /api/data/?title=Sample

🔒 .gitignore

This project excludes sensitive files with the following .gitignore:

client_secret.json
venv/
__pycache__/
*.pyc
db.sqlite3


