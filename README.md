# Banking Application

A Flask-based banking application with user authentication, account linking, and money transfer functionality.

## Features

- User registration and login
- Password reset functionality
- Account linking with bank details
- Balance checking
- Money transfer between UPI IDs
- Session management

## Setup Instructions

### Prerequisites
- Python 3.7+
- MongoDB installed and running on localhost:27017

### Installation

1. Clone or download the project
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start MongoDB service on your machine

4. Run the application:
   ```
   python app.py
   ```

5. Open your browser and go to: http://localhost:5000

## Database Structure

### User_details Collection
```json
{
  "Username": "string",
  "Email": "string", 
  "Phone": number,
  "Password": "string",
  "Link": boolean
}
```

### Account_details Collection
```json
{
  "Phone": number,
  "UPIID": "string",
  "UPIPIN": "string",
  "Balance": number
}
```

## Security Notes

⚠️ **This is a demo application. For production use, implement:**
- Password hashing (bcrypt)
- CSRF protection
- Input validation and sanitization
- Rate limiting
- HTTPS encryption
- Environment variables for sensitive data

## API Endpoints

- `/` - Home/Login page
- `/login` - Handle login
- `/signup` - User registration form
- `/create` - Process user registration
- `/forget` - Password reset form
- `/check` - Verify user for password reset
- `/reset` - Reset password
- `/link` - Link account with bank
- `/balance` - Show/hide balance
- `/transfer` - Transfer money form
- `/transaction` - Process money transfer
- `/logout` - Logout user
