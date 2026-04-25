# LADBS Test Applications - Salesforce Permit Management System

A web-based application for managing Salesforce Permit Applications, Submissions, and Reviews for the Los Angeles Department of Building and Safety (LADBS).

## Features

- **Create Permit Applications**: Create new permit applications in Salesforce with auto-populated default values
- **Complete Submissions**: Bulk complete all submissions for a given application number
- **Complete Reviews**: Bulk complete and approve all reviews for a given application number
- **Permit History**: View previously created permit applications in a table format
- **Conditional License Type**: Dynamic license type selection for Contractor roles

## Project Structure

```
├── backend/
│   └── api.py                 # FastAPI backend server
├── frontend/
│   ├── index.html            # Main HTML page
│   ├── app.js                # Frontend JavaScript
│   └── styles.css            # CSS styles
├── config/
│   ├── config.py             # General configuration
│   └── salesforce_config.py  # Salesforce credentials config
├── utils/
│   ├── driver_factory.py     # Selenium WebDriver factory
│   └── salesforce_client.py  # Salesforce API client wrapper
├── salesforce_console/        # Standalone Salesforce scripts
│   ├── create_permit_application.py
│   ├── update_submission_status.py
│   ├── update_review_status.py
│   └── ...
├── data/
│   └── permit_applications.csv  # Local storage for permit history
├── tests/                     # Pytest test files
├── reports/                   # Allure test reports
├── .env.example              # Example environment variables
├── requirements.txt          # Python dependencies
└── start_app.bat             # Windows batch file to start the app
```

## Prerequisites

- Python 3.10+
- Salesforce sandbox account with API access
- Git

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nithish-gitt/LADBS-Test-Applications.git
   cd LADBS-Test-Applications
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Salesforce credentials**
   
   Create a `.env` file in the project root:
   ```env
   SF_USERNAME=your_username@example.com
   SF_PASSWORD=your_password
   SF_SECURITY_TOKEN=your_security_token
   SF_DOMAIN=test
   ```

## Running the Application

### Using the batch file (Windows)
```bash
start_app.bat
```

### Manual startup

1. **Start the backend server**
   ```bash
   cd backend
   python api.py
   ```
   The API will be available at `http://localhost:8000`
   
   API documentation: `http://localhost:8000/docs`

2. **Start the frontend server**
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Open `http://localhost:8080` in your browser

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/permit-types` | Get available permit types from Salesforce |
| POST | `/api/permit-application` | Create a new permit application |
| POST | `/api/complete-submissions` | Complete all submissions for an application |
| POST | `/api/complete-reviews` | Complete all reviews for an application |
| GET | `/api/permit-history` | Get previously created permit applications |
| GET | `/api/default-values` | Get default form values |

## Usage

### Create Permit Application
1. Click "Create Permit Application" on the homepage
2. Fill in the form (default values are pre-populated):
   - Applicant Name
   - Address
   - Permit Type
   - Applicant Role
   - License Type (only for Contractor roles)
   - Use Class
3. Click "Create Permit Application"

### Complete Submissions
1. Click "Complete Submissions" on the homepage
2. Enter the Application Number
3. Click "Complete All Submissions"

### Complete Reviews
1. Click "Complete Reviews" on the homepage
2. Enter the Application Number
3. Click "Complete All Reviews"

## Salesforce Objects Used

- `MUSW__Application2__c` - Permit Applications
- `MUSW__Submission__c` - Submissions
- `MUSW__Review__c` - Reviews
- `MUSW__Application_Template__c` - Application Templates (Permit Types)
- `MUSW__Address__c` - Addresses
- `Contact` - Applicants
- `LACPS_External_License__c` - Contractor Licenses

## Technologies Used

- **Backend**: Python, FastAPI, simple-salesforce
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Testing**: Pytest, Selenium, Allure Reports

## License

This project is for internal testing purposes.

## Author

Nithish Vemula
