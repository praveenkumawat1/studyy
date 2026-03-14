# 🚀 STUDY TRACKER - REACT FRONTEND QUICK START

## ⚡ 5-Minute Quick Start

### Prerequisites (Check These First)
- ✅ MySQL running (`study_tracker_db` database created)
- ✅ Node.js installed (https://nodejs.org/)
- ✅ Python backend modules available

### Run These Commands

**Terminal 1 - Start API Server:**
```powershell
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

  Endpoints:
    POST   /api/auth/register      - Register new user
    POST   /api/auth/login         - Login user
    GET    /api/auth/user          - Get current user
    ...
```

**Terminal 2 - Start React Frontend:**
```bash
cd frontend
npm install
npm start
```

Expected output:
```
Compiled successfully!

You can now view study-tracker-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use: npm run build
```

**Open your browser to:** http://localhost:3000

---

## 🎨 What You'll See

### Login Page
```
┌────────────────────────────────────┐
│                                    │
│         📚 Study Tracker           │
│      Login to your account         │
│                                    │
│  Username [ ________________ ]     │
│  Password [ ________________ ]     │
│                                    │
│         [ LOGIN ]                  │
│                                    │
│  Don't have account? Create one    │
└────────────────────────────────────┘
```

### Registration Page (Click "Create one")
```
┌────────────────────────────────────┐
│     Create Account                 │
│   Join Study Tracker today         │
│                                    │
│  Full Name [ ________________ ]    │
│  Email [ ________________ ]        │
│  Phone [ ________________ ]        │
│  Password [ ________________ ]     │
│  Confirm [ ________________ ]      │
│                                    │
│  [ CREATE ACCOUNT ]                │
└────────────────────────────────────┘
```

### Dashboard (After Login)
```
┌───────────────────────────────────────────────────┐
│ 📚 Study Tracker   Welcome, Your Name    [YN]   ▼ │
└───────────────────────────────────────────────────┘

📈 Overview | ✏️ Add Session | 📊 Analytics

┌───────────────────────────────────────────────────┐
│  ⏱️ TOTAL HOURS    │  📚 SESSIONS   │  ⭐ PRODUCTIVITY  │
│     0.0 h        │      0        │     0/5           │
└───────────────────────────────────────────────────┘

📅 Today's Sessions
   (No sessions logged today)

✏️ Add Session
   Subject:     [ Dropdown ▼ ]
   Hours:       [ 2.5 ]
   Productivity: ⭐⭐⭐ (3/5)
   Notes:       [ Lorem ipsum... ]
   [ ✅ Log Session ]

📊 Analytics
   Subject Performance
   (Breakdown by subject)
```

---

## 📋 Step-by-Step Tutorial

### Step 1: Create Account
1. Click **"Create one"** link on login page
2. Fill in details:
   - Full Name: Your name
   - Email: your@email.com
   - Phone: 1234567890 (10 digits)
   - Password: SecurePass123 (uppercase, lowercase, number required)
   - Confirm: SecurePass123
3. Click **"Create Account"**
4. Auto-redirected to Dashboard ✅

### Step 2: Log a Study Session
1. Click **"✏️ Add Session"** tab
2. Select subject from dropdown (Math, Physics, Os, DBMS, etc.)
3. Enter hours studied (e.g., 2.5)
4. Adjust productivity slider (1-5 stars)
5. Add notes (optional)
6. Click **"✅ Log Session"**
7. Success message appears ✅

### Step 3: View Statistics
1. Back to **"📈 Overview"** tab
2. See updated statistics:
   - Total Hours This Week
   - Number of Sessions
   - Average Productivity
   - Subjects Tracked
3. Check **"Today's Sessions"** list

### Step 4: Check Analytics
1. Click **"📊 Analytics"** tab
2. See subject-wise breakdown:
   - Hours per subject
   - Sessions per subject
   - Productivity rating per subject
3. View weekly trends summary

---

## 🔑 Test Credentials

After registration, you can use any account you create.

**Example user (to create):**
```
Name: John Doe
Email: john@example.com
Phone: 9876543210
Password: TestPass123
```

---

## 📱 Features Overview

### ✨ User Features
- ✅ Create account with email validation
- ✅ Secure login
- ✅ Dashboard with personalized welcome
- ✅ Log study sessions
- ✅ Track productivity (1-5 rating)
- ✅ View statistics
- ✅ Subject-wise analytics
- ✅ Weekly exam readiness score
- ✅ AI recommendations
- ✅ Session history

### 🔒 Security Features
- ✅ PBKDF2-SHA256 password hashing
- ✅ JWT token authentication
- ✅ Secure password validation
- ✅ Email format validation
- ✅ Protected routes (dashboard requires login)
- ✅ Auto-logout on token expiration

### 🎨 UI Features
- ✅ Beautiful gradient Design
- ✅ Smooth animations
- ✅ Responsive layout (mobile, tablet, desktop)
- ✅ Card-based UI
- ✅ Color-coded statistics
- ✅ Star rating system
- ✅ Emoji icons
- ✅ Loading states
- ✅ Error messages
- ✅ Success notifications

---

## 🔧 API Endpoints Used

### Authentication
- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/user` - Get current user

### Sessions  
- `POST /api/sessions` - Log session
- `GET /api/sessions/today` - Get today's sessions
- `GET /api/sessions/week` - Get week's sessions

### Reports
- `GET /api/reports/weekly` - Get weekly report

### Analytics
- `GET /api/analytics/subjects` - Get subject performance

---

## ❌ Troubleshooting

### Issue: Port 3000 already in use
```powershell
# Use different port
$env:PORT=3001; npm start

# Or kill process using 3000 (Windows)
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: "Cannot find module" errors
```bash
cd frontend
rm -r node_modules
npm install
npm start
```

### Issue: API connection failed
- Check Terminal 1 running `python api_server.py`
- Verify no errors in API server output
- Check port 5000 is free
- Ensure MySQL is running

### Issue: Login fails
- Verify account was created successfully
- Check MySQL has data: `mysql study_tracker_db`
- Confirm username/password exactly

### Issue: Blank page after login
- Open DevTools: F12
- Check Console tab for errors
- Check Network tab (API calls)
- Kill both servers, restart

---

## 📁 Project Structure

```
study-ml-model/
├── frontend/                          ← React App
│   ├── public/index.html
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.js              ← Login page
│   │   │   ├── Register.js           ← Registration
│   │   │   └── Dashboard.js          ← Main dashboard
│   │   ├── components/
│   │   │   └── Navigation.js         ← Top nav bar
│   │   ├── styles/
│   │   │   ├── Auth.css              ← Login/Register styles
│   │   │   ├── Dashboard.css         ← Dashboard styles
│   │   │   └── index.css             ← Global styles
│   │   ├── services/
│   │   │   └── api.js                ← API client
│   │   ├── context/
│   │   │   └── AuthContext.js        ← Auth state
│   │   └── App.js
│   └── package.json
│
├── api_server.py                      ← Flask API (Python)
├── auth.py                            ← Authentication
├── db_operations.py                   ← Database operations
└── [Other Python modules]
```

---

## 📈 Next Steps

1. **Create account** → Register page
2. **Log sessions** → Dashboard "Add Session" tab
3. **Track progress** → Statistics on Overview tab
4. **Analyze performance** → Analytics tab
5. **Weekly insights** → Weekly report with recommendations

---

## ✅ Success Checklist

- [ ] MySQL database created
- [ ] Node.js installed
- [ ] API server starts without errors
- [ ] Frontend installs without errors
- [ ] Can open http://localhost:3000
- [ ] Can register new account
- [ ] Can login
- [ ] Can see dashboard
- [ ] Can log study session
- [ ] Can view statistics

---

## 💡 Tips

- **Bookmark:** Save http://localhost:3000 in favorites
- **Multiple Sessions:** Keep API and Frontend in separate terminals
- **Testing:** Create multiple test accounts to test multi-user
- **Development:** Use `npm start` for live reload on code changes
- **Mobile:** Open http://192.168.x.x:3000 from phone on same network

---

## 🆘 Need Help?

1. Check browser console: **F12 → Console tab**
2. Check API server output: Look at Terminal 1
3. Check network requests: **F12 → Network tab**
4. MySQL connection: `mysql -u root -proot study_tracker_db`
5. View this README again: See **step-by-step** section

---

## 🎉 You're All Set!

Your study tracker is ready to use. Log your first session and start tracking progress! 📚✨

