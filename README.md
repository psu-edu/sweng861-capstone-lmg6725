# Campus Health Appointment System 

**Name:** Lauren Gilbert
**Course:** SWENG 861 – Software Construction

## Project Description

The Campus Health Appointment System is a web application for university students and campus healthcare staff. The original project requirements include Doctor and Patient role-based access control, appointment-slot viewing, appointment booking and visit records, and SMS appointment confirmations through Twilio. The proposal also identifies PCP notification requests and appointment cancellation/rescheduling as nice-to-have features.

The current implementation expands on that foundation with separate patient and doctor workflows, structured provider information, appointment recommendations, and an AI-assisted scheduling workflow.

## Tech Stack

### Backend
- Python3
- Flask
- SQLAlchemy
- Flask-Limiter
- SQLite
- Okta OIDC

### Frontend
- React
- Vite
- JavaScript
- HTML / CSS

### External Services
- Okta for authentication
- Twilio for SMS appointment notifications
- Drift API for the AI scheduling assistant

### Development Tools
- Git
- GitHub
- Postman
- pytest
## External Services
- Okta authentication
- Twilio for SMS appointment notifications

# Repository Setup

Clone the repository steps
- git clone (repository url)
- cd (repository name)

Authentication

The application uses Okta for authentication. The frontend provides a Login with Okta button that redirects the user to Okta for authentication. After authentication, Okta redirects the user back to the application's callback endpoint.

### Patient Appointment Scheduling
- View available appointment slots
- Select a provider
- Filter available appointments by month
- Appointment availability up to 3 months in advance
- Monday through Friday appointment availability
- Book appointments
- View appointment details
- Prevent booking an already scheduled provider/time combination
- Cancel appointments
- Reschedule appointments

### Provider Information
- Providers are stored in SQLite
- Provider records include information used by the scheduling and recommendation workflows
- Appointment availability is generated from active providers and existing scheduled appointments

### Patient Profile
- View patient profile information
- Store and update a phone number for SMS appointment notifications

### Doctor Workflow
- Doctor Dashboard
- View all appointments
- Display patient names for appointments linked to user profiles
- Filter appointments by status
- Open visit records
- Review patient notes
- Add and update doctor notes
- Mark visits as completed

### Appointment Recommendations
Patients can request appointment recommendations by selecting:
- Service category
- Preferred time of day

The recommendation workflow uses provider service information and actual appointment availability. Booked provider/date/time combinations are excluded from recommendations.

### AI Scheduling Assistant
The recommendation page also includes a natural-language Scheduling Assistant. A patient can describe the type of appointment being requested, and the assistant classifies the request into a supported service category and scheduling preference before the standard recommendation workflow searches actual provider availability.

The Scheduling Assistant is intended only to assist with appointment classification and scheduling preferences. It does not provide medical diagnoses, treatment recommendations, or medical advice.

#### Drift Development Fallback
The application is integrated with the provided Drift API. When the external Drift service is unavailable during development, the backend can use a clearly identified development fallback classifier so the scheduling workflow can still be tested. The fallback does not create appointment availability. Appointment recommendations continue to use provider and appointment data from the application.

### SMS Notifications
- Twilio integration
- SMS is triggered after a successful appointment booking when the patient has a phone number stored

The current Twilio trial environment uses a predefined appointment-reminder template. The sample date/time contained in that trial message is controlled by the Twilio trial template rather than the appointment data stored by the application.

### Primary Care Provider Notification Request
Patients may request PCP notification and provide PCP contact information during booking.

The application displays an authorization notice explaining that selecting the request does not automatically send appointment information. The current workflow states that physical authorization must be handled through the Campus Health office before information is sent.

## User Workflows

### Patient Workflow
1. Login with Okta.
2. View or update profile information and phone number.
3. Choose either manual appointment availability or appointment recommendations.
4. Select an available appointment.
5. Complete the booking form.
6. View booked appointments and appointment details.
7. Cancel or reschedule appointments when appropriate.

### AI-Assisted Patient Workflow
1. Open Find a Recommended Appointment.
2. Select scheduling preferences or describe the requested appointment to the Scheduling Assistant.
3. The scheduling request is classified into supported scheduling values.
4. The recommendation endpoint searches actual provider availability.
5. Select a recommended appointment.
6. Continue to the standard booking page.

### Doctor Workflow
1. Login with a Doctor-role Okta account.
2. Open the Doctor Dashboard.
3. View all appointments.
4. Filter appointments by visit status.
5. Open a visit record.
6. Review patient information and patient notes.
7. Add or update doctor notes.
8. Mark a visit as completed.

## Repository Setup

Clone the repository: git clone https://github.com/psu-edu/sweng861-capstone-lmg6725.git

- cd sweng861-capstone-lmg6725


## Running the Backend

Open Command Prompt and navigate to the backend folder: cd src/server
Create a virtual environment if needed:
python -m venv venv
Activate the virtual environment on Windows:
venv\Scripts\activate

Install the required packages:

pip install -r requirements.txt

Start the Flask application from the virtual environment:

python main.py

# Running the Frontend
Open a second terminal and navigate to the frontend: cd src/client
Install frontend dependencies:
npm install
Start Vite:
npm run dev

## Environment Variables

Create the backend `.env` file used by the project. Do not commit real credentials or tokens to source control.

### Backend

OKTA_CLIENT_ID=<Okta client ID>
OKTA_CLIENT_SECRET=<Okta client secret>
OKTA_ISSUER=<Okta issuer>
OKTA_REDIRECT_URL=http://localhost:5000/authorize/callback
FRONTEND_URL=http://localhost:5173
DRIFT_API_KEY=<Drift API key>
TWILIO_ACCOUNT_SID=<Twilio account SID>
TWILIO_AUTH_TOKEN=<Twilio auth token>
TWILIO_PHONE_NUMBER=<Twilio sending phone number>


### Frontend
- VITE_BACKEND_URL = http://localhost:5000
## Testing
The repository includes pytest coverage for authentication middleware, Drift client/validator behavior, API behavior, appointments, authentication routes, and prompt routes.

Run tests from `src/server` with the virtual environment active:
python -m pytest -v
## Known Development Limitations
- The external Drift service may be unavailable. The application currently supports a clearly labeled development fallback for the AI-assisted scheduling workflow.
- Twilio trial messaging uses a predefined appointment-reminder template, so the message text may contain sample date/time information controlled by Twilio.
