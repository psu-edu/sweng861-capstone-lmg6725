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
- HTML / CSS
- React
- Vite
- JavaScript
- Twilio

### Dev tools
- Git
- GitHub
- Postman

## External Services
- Okta authentication
- Twilio for SMS appointment notifications

# Repository Setup

Clone the repository steps
- git clone (repository url)
- cd (repository name)

Authentication

The application uses Okta for authentication. The frontend provides a Login with Okta button that redirects the user to Okta for authentication. After authentication, Okta redirects the user back to the application's callback endpoint.

### Appointment Scheduling
- View available appointmint slots
- Provider selection
- Appointment availability up to 3 montsh in advance
- Monday-Friday appointment availability
- Book appointmints
- View appointment details
- Cancel appointments
- Reschedule appointments
- Prevent booking an already scheduled provider/time

### Patient Profile
- View profile information
- Add or update phone number
- Phone number stored for SMS notifications

### SMS Notifications
- Twilio integration
- SMS triggered after successful appointment booking.
The current Twilio trial environment uses a predefined appointment
reminder template. The sample date/time contained in the Twilio trial
message is controlled by the trial template rather than the
appointment data stored by the application.

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
- FRONTEND_URL = http://localhost:5173
- TWILIO_ACCOUNT_SID = twilio_account_sid
- TWILIO_AUTH_TOKEN = auth_token
- TWILIO_PHONE_NUMBER = phone_number

# Enivronment Variables - frontend
- VITE_BACKEND_URL = http://localhost:5000
