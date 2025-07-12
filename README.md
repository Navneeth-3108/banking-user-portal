# Flask Banking Web App

A secure and user-friendly banking web application built using Flask, MongoDB, and Flask-Mail. This application includes features like user signup with email OTP verification, login/logout, password reset, account linking, balance view, and fund transfer using UPI ID.

---

## 🔧 Features

- User registration with email OTP verification
- Secure login and session management with bcrypt password hashing
- Password reset using email verification
- Account linking with bank details
- Balance view and hide feature
- Secure money transfer between accounts via UPI ID
- Email notifications using Gmail SMTP
- MongoDB backend for storing user and account details
- Input validation for phone numbers, emails, and UPI PINs

---

## 🛠 Tech Stack

- **Backend**: Flask (Python)
- **Database**: MongoDB (via PyMongo)
- **Email Service**: Flask-Mail (Gmail SMTP)
- **Security**: bcrypt for password hashing

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Navneeth-3108/banking-user-portal.git
cd banking-user-portal
```

### 2. Set up a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add your email credentials:

```env
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MONGODB_URI=mongodb://localhost:27017/
```

**Important**: Never commit your `.env` file to version control!

### 5. Run MongoDB

Ensure MongoDB is installed and running locally on default port `27017`.

```bash
mongod
```

### 6. Run the app

```bash
python app.py
```

The app will be available at: [http://localhost:5000](http://localhost:5000)

---

## 🖥️ Usage

1. **Registration**: Create a new account with email verification
2. **Login**: Access your account with email and password
3. **Link Bank Account**: Add your bank details and UPI ID
4. **View Balance**: Check your account balance (with hide/show option)
5. **Transfer Funds**: Send money to other users using their UPI ID
6. **Password Reset**: Reset forgotten passwords using email verification

---

## 📁 Folder Structure

```
banking-user-portal/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── static/                 # Static assets
│   └── style.css           # Main stylesheet
└── templates/              # HTML templates
    ├── index.html          # Login page
    ├── dashboard.html      # Main dashboard
    ├── welcome.html        # Welcome page
    ├── forget.html         # Forgot password
    ├── reset.html          # Password reset
    ├── create.html         # Account creation
    ├── otp.html            # OTP verification (signup)
    ├── pwotp.html          # OTP verification (password reset)
    └── transaction.html    # Transaction page
```

---

## 📧 SMTP Email Configuration

In `app.py`, replace with your own Gmail credentials or app password:

```python
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

Enable **less secure app access** or use **App Passwords** if using 2FA.

---

## 📦 Dependencies

```
Flask==2.3.3           # Web framework
pymongo==4.7.0         # MongoDB driver
Flask-Mail==0.9.1      # Email functionality
dnspython==2.4.2       # DNS toolkit (required by pymongo)
bcrypt==4.0.1          # Password hashing library
```

Install all dependencies with: `pip install -r requirements.txt`

---

## 🔒 Security Notes

⚠️ **Security Features Implemented:**

- **Secure Password Storage** - Passwords are hashed using bcrypt with salt
- **Session Management** - Secure session handling with server-side validation
- **OTP Verification** - Email-based OTP for account creation and password reset
- **Input Validation** - Phone number, email, and UPI PIN validation
- **Duplicate Prevention** - Prevents duplicate usernames, emails, and phone numbers

⚠️ **Additional Security Considerations for Production:**

- Use environment variables for sensitive data (already recommended)
- Enable 2FA and use App Passwords for Gmail
- Implement proper input validation and sanitization
- Add rate limiting for login attempts
- Use HTTPS in production
- Implement CSRF protection
- Add proper logging and monitoring

---

## 🔐 Password Security Implementation

This application implements secure password handling using bcrypt:

### Password Hashing
```python
import bcrypt

# During registration - hash the password
password = request.form['password'].encode('utf-8')
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

# During login - verify the password
if user and bcrypt.checkpw(password, user["Password"]):
    # Login successful
```

### Security Features
- **Salt Generation**: Each password gets a unique salt
- **Bcrypt Algorithm**: Industry-standard password hashing
- **Verification**: Secure password comparison without storing plain text
- **Session Security**: Proper session management and cleanup

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

---

## 📝 License

This project is for educational purposes. Please use responsibly.

---

## 📞 Contact

For questions or support, please create an issue in this repository.

---

## 🔗 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/` | Show login page | None |
| `POST` | `/login` | User login | `email`, `password` |
| `POST` | `/logout` | User logout | None |
| `GET` | `/signup` | Show signup page | None |
| `POST` | `/create` | Create new user account | `username`, `email`, `phone`, `password` |

### Password Management

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `GET` | `/forget` | Show forgot password page | None |
| `POST` | `/check` | Verify user email for password reset | `email` |
| `POST` | `/pwotp` | Verify OTP for password reset | `otp` |
| `POST` | `/pwresend` | Resend password reset OTP | None |
| `POST` | `/reset` | Reset user password | `password1`, `password2` |

### OTP Verification

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/otp` | Verify OTP for account creation | `otp` |
| `POST` | `/resend` | Resend signup OTP | None |

### Account Management

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/link` | Link bank account | None |
| `GET/POST` | `/dashboard` | Show user dashboard | None |
| `POST` | `/balance` | Show account balance | None |
| `POST` | `/hide` | Hide account balance | None |

### Transaction Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/transfer` | Show transfer page | None |
| `POST` | `/transaction` | Process money transfer | `UPIID`, `UPIPIN`, `amount` |

### Navigation

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/login-page` | Return to login page | None |

### Request/Response Examples

#### User Registration
```bash
# POST /create
curl -X POST http://localhost:5000/create \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&email=john@example.com&phone=1234567890&password=mypassword"
```

#### User Login
```bash
# POST /login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=john@example.com&password=mypassword"
```

#### Password Reset Flow
```bash
# Step 1: Request password reset
curl -X POST http://localhost:5000/check \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "email=john@example.com"

# Step 2: Verify OTP
curl -X POST http://localhost:5000/pwotp \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "otp=123456"

# Step 3: Reset password
curl -X POST http://localhost:5000/reset \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "password1=newpassword&password2=newpassword"
```

#### Money Transfer
```bash
# POST /transaction
curl -X POST http://localhost:5000/transaction \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "UPIID=recipient@bank&UPIPIN=1234&amount=1000"
```

### Session Management
- All authenticated routes require active session
- Session stores: `phone`, `name`, `email`
- Sessions are cleared on logout
- Temporary sessions for OTP verification store: `otp`, `username`, `email`, `phone`, `password`

### Error Handling
- Invalid credentials return error messages to login page
- Form validation errors display on respective forms
- Session expiry redirects to login page
- Database errors handled gracefully

---

## 🔄 Application Workflows

### User Registration Flow
1. **Sign Up** → Enter username, email, phone, password → `/create`
2. **Email Sent** → OTP sent to user's email
3. **OTP Verification** → Enter OTP → `/otp` → Account created
4. **Login** → Use email and password → `/login`

### Password Reset Flow
1. **Forgot Password** → Enter email → `/check`
2. **Email Verification** → OTP sent to email
3. **OTP Verification** → Enter OTP → `/pwotp`
4. **Reset Password** → Enter new password → `/reset`
5. **Login** → Use new credentials

### Banking Operations Flow
1. **Login** → Access dashboard or welcome page
2. **Link Account** → Connect bank details (if not linked)
3. **Dashboard Access** → View balance, transfer money, logout
4. **Money Transfer** → Enter UPI ID, amount, PIN → Transaction complete

---
