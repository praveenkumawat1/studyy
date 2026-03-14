DATABASE INTEGRATION GUIDE
==========================

AI-Based Study Tracker with MySQL Database

## 📋 WHAT'S NEW

The Study Tracker now includes:
✓ MySQL database integration
✓ User authentication (register/login)
✓ Secure password hashing
✓ User-specific data storage
✓ Session management
✓ Complete data persistence
✓ Account management
✓ Data history and analytics

## 🗄️ DATABASE STRUCTURE

### Tables Created:

1. **users**
   - user_id (Primary Key)
   - username (Unique)
   - email (Unique)
   - password (Hashed)
   - full_name
   - created_at
   - last_login
   - is_active

2. **study_sessions**
   - session_id (Primary Key)
   - user_id (Foreign Key)
   - subject
   - hours_studied
   - productivity_level (1-5)
   - notes
   - session_date
   - session_time
   - Indexes for fast queries

3. **subject_performance**
   - performance_id (Primary Key)
   - user_id (Foreign Key)
   - subject
   - total_hours
   - total_sessions
   - avg_productivity
   - first_session_date
   - last_session_date
   - Unique constraint: user + subject

4. **weekly_reports**
   - report_id (Primary Key)
   - user_id (Foreign Key)
   - week_start
   - week_end
   - total_hours
   - total_sessions
   - avg_productivity
   - exam_readiness_score
   - recommendations (JSON)

5. **timetables**
   - timetable_id (Primary Key)
   - user_id (Foreign Key)
   - week_start
   - timetable_data (JSON)
   - created_at

6. **goals**
   - goal_id (Primary Key)
   - user_id (Foreign Key)
   - subject
   - target_hours
   - target_sessions
   - deadline
   - achieved

## 🚀 INSTALLATION STEPS

### Step 1: Install MySQL

**Windows:**
1. Download from https://dev.mysql.com/downloads/mysql/
2. Run installer (MSI)
3. Choose "Developer Default" setup
4. Configure MySQL Server
5. Port: 3306 (default)
6. MySQL Root Password: Leave blank (or set one)

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
```

**Mac:**
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### Step 2: Install Python Packages

```bash
pip install mysql-connector-python
pip install pandas scikit-learn numpy joblib
```

Or use the setup script:
```bash
python setup_database.py
```

### Step 3: Initialize Database

```bash
python setup_database.py
```

This will:
- Verify MySQL connection
- Install missing Python packages
- Create study_tracker_db database
- Create all required tables

## 📁 NEW FILES CREATED

1. **db_config.py**
   - Database connection configuration
   - DatabaseSetup class for initialization
   - Table creation scripts

2. **auth.py**
   - UserAuthentication class
   - PasswordHasher for secure hashing
   - SessionManager for session management
   - User registration and login

3. **db_operations.py**
   - StudySessionDB - CRUD for sessions
   - SubjectPerformanceDB - Subject analytics
   - WeeklyReportDB - Report storage
   - TimetableDB - Schedule storage

4. **setup_database.py**
   - Automated database setup
   - MySQL installation guide
   - Package verification

5. **study_tracker_app_db.py**
   - Main app with database integration
   - Login/Register UI
   - User authentication flow
   - Database operations integration

## 🔐 SECURITY FEATURES

✓ Password Hashing
  - PBKDF2-SHA256
  - 100,000 iterations
  - Random salt (32 bytes)

✓ SQL Injection Prevention
  - Parameterized queries
  - No string concatenation

✓ Account Security
  - Password strength validation
  - Email format validation
  - Username format validation
  - Last login tracking

✓ Data Integrity
  - Foreign key constraints
  - Unique constraints
  - Type checking

## 📋 USAGE

### First Time Setup

```bash
# 1. Install dependencies
python setup_database.py

# 2. Start the application
python study_tracker_app_db.py

# 3. Register a new account
# 4. Start logging study sessions
```

### Using the Application

**Register New User:**
1. Run app
2. Select "Register"
3. Enter: username, email, password, name
4. Password must have: uppercase, lowercase, number, 6+ chars

**Login:**
1. Run app
2. Select "Login"
3. Enter username and password

**Log Study Session:**
1. Select "Daily Tracking"
2. Select "Add new study session"
3. Enter: subject, hours, productivity (1-5), notes

**View Reports:**
1. Select "Weekly Report"
2. Auto-calculates exam readiness
3. Save to database

**Account Settings:**
1. Change password
2. View profile
3. Delete account

## 🔧 CONFIGURATION

Edit `db_config.py` to change MySQL settings:

```python
DB_CONFIG = {
    'host': 'localhost',        # MySQL server host
    'user': 'root',             # MySQL user
    'password': '',             # MySQL password
    'database': 'study_tracker_db',
    'port': 3306                # MySQL port
}
```

## 📊 DATABASE QUERIES

### Get User's Sessions
```sql
SELECT * FROM study_sessions 
WHERE user_id = ? AND session_date = ?
```

### Get Subject Performance
```sql
SELECT subject, total_hours, avg_productivity 
FROM subject_performance 
WHERE user_id = ?
```

### Get Weekly Reports
```sql
SELECT * FROM weekly_reports 
WHERE user_id = ? 
ORDER BY week_start DESC
```

## 🐛 TROUBLESHOOTING

### Issue: "Cannot connect to MySQL"
**Solutions:**
1. Verify MySQL is running
2. Check host/port in db_config.py
3. Verify user credentials
4. Windows: Open Services (services.msc) and start MySQL

### Issue: "Database does not exist"
**Solution:**
```bash
python setup_database.py
```

### Issue: "Table already exists"
**Solution:**
- Normal message, ignore it
- Or drop and recreate: `DROP DATABASE study_tracker_db;`

### Issue: "Access denied for user 'root'"
**Solution:**
1. Windows: Reinstall MySQL without password
2. Linux: Use `sudo mysql`
3. Update password in db_config.py

## 📈 DATA PERSISTENCE

All data is now persistently stored in MySQL:

✓ User accounts
✓ Study sessions
✓ Subject performance metrics
✓ Weekly reports
✓ Generated timetables
✓ Progress history

Data survives:
- Application restarts
- System restarts
- Multiple user sessions

## 🔄 FEATURE COMPARISON

### Before (CSV-based)
- Single user
- Local CSV files
- No security
- Lost data if files deleted

### After (MySQL)
- Multiple users
- Secure database
- User authentication
- Password hashing
- Account management
- Data analytics
- Query-able data
- Backup capability

## 📚 API DOCUMENTATION

### Authentication (auth.py)

```python
# Register
success, msg = UserAuthentication.register_user(
    username, email, password, full_name
)

# Login
user_id, msg = UserAuthentication.login_user(username, password)

# Change password
success, msg = UserAuthentication.change_password(
    user_id, old_password, new_password
)

# Get user info
user_info = UserAuthentication.get_user_info(user_id)
```

### Study Sessions (db_operations.py)

```python
# Add session
success, msg = StudySessionDB.add_session(
    user_id, subject, hours, productivity_level, notes
)

# Get today's sessions
sessions = StudySessionDB.get_today_sessions(user_id)

# Get week sessions
sessions = StudySessionDB.get_week_sessions(user_id)

# Delete session
success = StudySessionDB.delete_session(user_id, session_id)
```

### Subject Performance

```python
# Update performance
SubjectPerformanceDB.update_subject_performance(
    user_id, subject, hours, productivity
)

# Get all subjects
performance = SubjectPerformanceDB.get_subject_performance(user_id)
```

### Weekly Reports

```python
# Save report
WeeklyReportDB.save_report(
    user_id, week_start, week_end, 
    total_hours, total_sessions, 
    avg_productivity, exam_readiness_score, 
    recommendations
)

# Get latest report
report = WeeklyReportDB.get_latest_report(user_id)
```

## 🎓 BENEFITS

1. **Multi-User Support**
   - Each student has own account
   - Isolated data
   - Privacy guaranteed

2. **Data Persistence**
   - All data kept permanently
   - Historical analysis possible
   - Long-term tracking

3. **Security**
   - Encrypted passwords
   - Secure login
   - Account management

4. **Analytics**
   - Query historical data
   - Generate insights
   - Track progress over time

5. **Scalability**
   - Supports many users
   - Fast queries with indexes
   - Room for growth

## 📞 SUPPORT

### Check Database Status
```bash
mysql -u root
SHOW DATABASES;
USE study_tracker_db;
SHOW TABLES;
SELECT COUNT(*) FROM users;
```

### Backup Database
```bash
mysqldump -u root study_tracker_db > backup.sql
```

### Restore Database
```bash
mysql -u root study_tracker_db < backup.sql
```

## 🎉 NEXT STEPS

1. ✓ Run setup_database.py
2. ✓ Register a new account
3. ✓ Log daily study sessions
4. ✓ View weekly reports
5. ✓ Track improvement over time

---

**Database Version**: 1.0.0
**Last Updated**: March 13, 2026
**Status**: Production Ready

Happy studying! 📚🎓
