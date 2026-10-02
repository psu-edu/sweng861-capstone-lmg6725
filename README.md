# Campus Health Appointment System 

**Name:** Lauren Gilbert
**Course:** SWENG 861 – Software Construction

## Project Description
The Campus Health Appointment System is a web application that allows university students to securely schedule appointments with the campus health center. Patients can view available appointment slots and receive SMS confirmations, while doctors can access authorized visit records through role-based access controls. **

## Tech Stack:

### Backend
- Python3
- Flask
- SQLAlchemy
- Flask-Limiter
- SQLite
- Okta OIDC

### Frontend
- HTML
- React
- Vite
- JavaScript

### Dev tools
- Git
- GitHub
- Postman

# Repository Setup

Clone the repository steps
- git clone (repository url)
- cd (repository name)

Authentication

The application uses Okta for authentication. The frontend provides a Login with Okta button that redirects the user to Okta for authentication. After authentication, Okta redirects the user back to the application's callback endpoint.

# Running the Application

Open Command Prompt and navigate to the backend folder: cd src/server
python -m venv venv
venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Start the Flask application from the virtual environment:

python main.py

# Running the Frontend
Open a second terminal and navigate to the frontend: cd src/client
npm install
npm run dev

# Environment Variables - Backend
- OKTA_CLIENT_ID = client-id from OKTA
- OKTA_CLIENT_SECRET = client-secret from OKTA
- OKTA_ISSUER = okta-issuer from OKTA
- OKTA_REDIRECT_URL = http://localhost:5000/authorize/callback
- DRIFT_API_KEY = insert your api key
FRONTEND_URL=http://localhost:5173
# Enivronment Variables - frontend
- VITE_BACKEND_URL = http://localhost:5000