# REACT FRONTEND SETUP & DEPLOYMENT GUIDE

## Quick Start

### Step 1: Install Node.js
If you don't have Node.js installed:
- Download from: https://nodejs.org/
- Install Node.js (includes npm)
- Verify installation: `node -v` and `npm -v`

### Step 2: Install Frontend Dependencies
```bash
cd frontend
npm install
```

### Step 3: Start API Server (Terminal 1)
```bash
python api_server.py
```

Expected output:
```
======================================================================
STUDY TRACKER - API SERVER
======================================================================

✓ Flask API Server Starting...
  API URL: http://localhost:5000/api
  Frontend: http://localhost:3000
```

### Step 4: Start React Frontend (Terminal 2)
```bash
cd frontend
npm start
```

The app will automatically open at `http://localhost:3000`

---

## Project Structure

```
study-ml-model/
├── frontend/                          # React.js Frontend
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── components/
│   │   │   └── Navigation.js          # Top nav with user menu
│   │   ├── pages/
│   │   │   ├── Login.js               # Clean login page
│   │   │   ├── Register.js            # Registration with validation
│   │   │   └── Dashboard.js           # Main study tracker dashboard
│   │   ├── context/
│   │   │   └── AuthContext.js         # Authentication state
│   │   ├── services/
│   │   │   └── api.js                 # API client
│   │   ├── styles/
│   │   │   ├── index.css              # Global styles
│   │   │   ├── Auth.css               # Login/register styles
│   │   │   ├── Navigation.css         # Nav bar styles
│   │   │   └── Dashboard.css          # Dashboard styles
│   │   ├── App.js                     # Main component with routing
│   │   └── index.js                   # Entry point
│   ├── package.json
│   └── README.md
│
├── api_server.py                      # Flask API Backend
├── auth.py                            # Authentication module
├── db_operations.py                   # Database operations
├── daily_tracker.py                   # Daily tracking logic
├── weekly_report.py                   # Report generation
├── db_config.py                       # Database config
├── setup_database.py                  # Database setup
└── [Other ML/tracking Python files]
```

---

## Frontend Features

### 1. Login Page
```
┌─────────────────────────────┐
│           📚 Study Tracker   │
│      Login to your account   │
│                             │
│  Username: [___________]    │
│  Password: [___________]    │
│                             │
│     [    LOGIN    ]          │
│                             │
│ Don't have account? Sign Up │
└─────────────────────────────┘
```

**Features:**
- Clean, centered card UI
- Email/password validation
- "Create account" link to registration
- Loading spinner on submit
- Error message display
- Auto-redirect to dashboard on success

### 2. Registration Page
```
┌─────────────────────────────┐
│      Create Account          │
│    Join Study Tracker today  │
│                             │
│  Name:      [___________]   │
│  Email:     [___________]   │
│  Phone:     [___________]   │
│  Password:  [___________]   │
│  Confirm:   [___________]   │
│                             │
│  [  CREATE ACCOUNT  ]        │
│                             │
│ Already registered? Login    │
└─────────────────────────────┘
```

**Features:**
- Full name, email, phone number inputs
- Strong password validation
  - At least 6 characters
  - Uppercase letter required
  - Lowercase letter required
  - Number required
- Password confirmation matching
- Real-time validation feedback
- Phone number formatting (10 digits)

### 3. Dashboard Page

#### Top Navigation
```
┌───────────────────────────────────────────────┐
│ 📚 Study Tracker   Welcome, John Smith   [JM] │
│                                           ▼   │
└───────────────────────────────────────────────┘
                          ┌──────────────┐
                          │ Dashboard    │
                          │ Settings     │
                          │ ─────────────│
                          │ Logout       │
                          └──────────────┘
```

**Features:**
- Study Tracker logo with brand
- Welcome message: "Welcome, {User Name}"
- User avatar (first letter)
- Dropdown menu
- Quick navigation

#### Dashboard Tabs

**📈 Overview Tab:**
- Statistics cards:
  - ⏱️ Total Hours This Week
  - 📚 Study Sessions
  - ⭐ Average Productivity
  - 🎯 Subjects Count

- Today's Sessions:
  - Subject name
  - Time & duration
  - Productivity rating (stars)
  - Notes preview

- Weekly Summary:
  - Exam readiness score (%)
  - Consistency metric (%)
  - AI recommendations

**✏️ Add Session Tab:**
- Form to log new session:
  - Subject dropdown (Math, Physics, Os, DBMS, etc.)
  - Hours studied input
  - Productivity slider (1-5 stars)
  - Session notes textarea
  - Submit button
  - Success/error messages

**📊 Analytics Tab:**
- Subject Performance Cards:
  - Hours studied per subject
  - Number of sessions
  - Average productivity per subject

- Weekly Trends:
  - Total sessions count
  - Total hours tracked
  - Average productivity rating

---

## API Endpoints

### Authentication

**POST /api/auth/register**
```javascript
Request:
{
  "username": "john_doe",
  "email": "john@example.com",
  "phone": "9876543210",
  "password": "SecurePass123"
}

Response (201):
{
  "success": true,
  "message": "Registration successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "john_doe"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**POST /api/auth/login**
```javascript
Request:
{
  "username": "john_doe",
  "password": "SecurePass123"
}

Response (200):
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "john_doe"
  },
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Study Sessions

**POST /api/sessions**
```javascript
Request (with Bearer token):
{
  "subject": "Mathematics",
  "hours_studied": 2.5,
  "productivity_level": 4,
  "notes": "Completed calculus chapter 5",
  "session_date": "2026-03-13",
  "session_time": "14:30:00"
}

Response (201):
{
  "success": true,
  "message": "Session added successfully",
  "session_id": 42
}
```

**GET /api/sessions/today**
**GET /api/sessions/week**
**GET /api/sessions/month**

Response:
```javascript
{
  "success": true,
  "sessions": [
    {
      "session_id": 42,
      "subject": "Mathematics",
      "hours_studied": 2.5,
      "productivity_level": 4,
      "notes": "Completed chapter 5",
      "session_date": "2026-03-13",
      "session_time": "14:30:00"
    }
  ]
}
```

### Reports

**GET /api/reports/weekly**
```javascript
Response:
{
  "success": true,
  "report": {
    "total_hours": 15.5,
    "total_sessions": 8,
    "avg_productivity": 3.8,
    "exam_readiness_score": 72,
    "consistency": 0.65,
    "recommendations": [
      "Increase study hours for Physics",
      "Maintain consistency in Mathematics",
      "Try active recall for Biology"
    ]
  }
}
```

### Analytics

**GET /api/analytics/subjects**
```javascript
Response:
{
  "success": true,
  "subjects": [
    {
      "subject": "Mathematics",
      "total_hours": 8.5,
      "total_sessions": 5,
      "avg_productivity": 4.0
    },
    {
      "subject": "Physics",
      "total_hours": 7.0,
      "total_sessions": 3,
      "avg_productivity": 3.7
    }
  ]
}
```

---

## Complete Workflow

### 1. First Time Setup
```bash
# Backend setup (one time)
python setup_database.py          # Initialize MySQL database

# Install Python API dependencies
pip install flask flask-cors PyJWT

# Install Node.js (if not installed)
# Download from https://nodejs.org/

# Install React dependencies
cd frontend
npm install
```

### 2. Daily Usage
```bash
# Terminal 1: Start API Server
python api_server.py
# Output: Running on http://localhost:5000

# Terminal 2: Start React Frontend
cd frontend
npm start
# Opens http://localhost:3000 automatically
```

### 3. User Flow

1. **Register**
   - Click "Create account" on login page
   - Fill in all details (name, email, phone, password)
   - System validates input
   - Account created, automatically logged in
   - Redirected to dashboard

2. **Login**
   - Enter username/email and password
   - System authenticates using MySQL
   - JWT token issued
   - Redirected to dashboard

3. **Dashboard Usage**
   - View welcome message
   - See statistics (hours, sessions, productivity)
   - Log study sessions (Overview tab → Go to Add Session tab)
   - View analytics and trends

4. **Track Progress**
   - Daily: Log study sessions
   - Weekly: Check exam readiness score
   - View personalized recommendations
   - Analyze subject-wise performance

---

## Environment Configuration

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Backend (api_server.py)
```python
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
```

⚠️ **IMPORTANT for Production:**
- Change JWT_EXPIRATION_DELTA
- Set secure SECRET_KEY
- Use HTTPS
- Enable rate limiting
- Set CORS allowed origins

---

## Troubleshooting

### Issue: Port 5000 already in use
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID)
taskkill /PID <PID> /F

# Or change Flask port in api_server.py
app.run(port=5001)
```

### Issue: Port 3000 already in use
```bash
# Use different port
PORT=3001 npm start
```

### Issue: CORS errors
- Ensure `flask-cors` is installed
- Check API_URL in frontend matches backend address
- Verify backend is running on correct port

### Issue: Login fails
- Check MySQL is running
- Verify database is initialized (`python setup_database.py`)
- Check credentials in db_config.py
- Look for error messages in backend console

### Issue: Frontend won't load
- Clear browser cache: Ctrl+Shift+Delete
- Check Node.js version: `node -v` (should be 14+)
- Delete `node_modules`, reinstall: `npm install`
- Check port 3000 is free

---

## Development Tips

### Enable Debug Mode
```bash
# Frontend
npm start             # Already in development mode

# Backend
# Set FLASK_ENV=development in terminal
set FLASK_ENV=development  # Windows
export FLASK_ENV=development  # Mac/Linux
python api_server.py
```

### View API Documentation
```bash
# Visit health check
curl http://localhost:5000/api/health

# Response:
# {
#   "status": "ok",
#   "message": "Study Tracker API is running"
# }
```

### Database Queries
```bash
# Connect to MySQL
mysql -h localhost -u root -proot study_tracker_db

# View all users
SELECT * FROM users;

# View sessions for user ID 1
SELECT * FROM study_sessions WHERE user_id = 1;

# View weekly reports
SELECT * FROM weekly_reports;
```

---

## Features Implemented

✅ Beautiful React.js UI
✅ User Registration & Login
✅ JWT Authentication
✅ Study Session Logging
✅ Daily/Weekly Statistics
✅ Subject Performance Analytics
✅ Exam Readiness Scoring
✅ Productivity Tracking
✅ Responsive Design
✅ Error Handling
✅ Loading States
✅ Form Validation
✅ User Dashboard
✅ Session Management
✅ MySQL Data Persistence
✅ RESTful API

---

## Next Steps

After setup:
1. Create user account
2. Log some study sessions
3. Check dashboard statistics
4. Review weekly reports
5. Analyze subject performance

---

## Support

For issues:
1. Check browser console (F12)
2. Check backend terminal output
3. Verify MySQL is running
4. Check port 5000 and 3000 are free
5. Review API endpoint documentation above

Happy studying! 📚✨
