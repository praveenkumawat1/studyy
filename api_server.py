"""
Flask API Backend for Study Tracker
Connects React frontend with MySQL database
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
import os
import sys
from datetime import datetime, timedelta

# Add parent directory to path to import local modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from auth import UserAuthentication, SessionManager
from db_config import DatabaseConfig
from db_operations import StudySessionDB, SubjectPerformanceDB, WeeklyReportDB, TimetableDB
from daily_tracker import DailyStudyTracker
from weekly_report import WeeklyReportGenerator

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=7)

# Initialize classes
session_manager = SessionManager()
study_db = StudySessionDB()
subject_db = SubjectPerformanceDB()
report_db = WeeklyReportDB()
timetable_db = TimetableDB()
daily_tracker = DailyStudyTracker()
report_generator = WeeklyReportGenerator()

# ============================================================================
# Helper Functions
# ============================================================================

def token_required(f):
    """Decorator to verify JWT token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'success': False, 'message': 'Token missing'}), 401
        
        try:
            # Remove 'Bearer ' prefix if present
            if token.startswith('Bearer '):
                token = token[7:]
            
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user_id = data['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'success': False, 'message': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'success': False, 'message': 'Invalid token'}), 401
        
        return f(current_user_id, *args, **kwargs)
    
    return decorated

def generate_token(user_id):
    """Generate JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + app.config['JWT_EXPIRATION_DELTA']
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

# ============================================================================
# Authentication Endpoints
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register new user"""
    data = request.get_json()
    
    try:
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        password = data.get('password', '')
        
        if not all([username, email, phone, password]):
            return jsonify({
                'success': False,
                'message': 'All fields are required'
            }), 400
        
        # Register user
        register_result = UserAuthentication.register_user(username, email, password, username)
        
        # Handle tuple response from register_user
        if isinstance(register_result, tuple):
            success, message = register_result
            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
            # Need to get the user_id from database
            connection = DatabaseConfig.get_connection()
            cursor = connection.cursor()
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            user_result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if not user_result:
                return jsonify({
                    'success': False,
                    'message': 'User registration failed'
                }), 500
            user_id = user_result[0]
        else:
            user_id = register_result
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': 'Registration failed. Username or email already exists.'
                }), 400
        
        # Get user info
        user_info = UserAuthentication.get_user_info(user_id)
        
        if not user_info:
            return jsonify({
                'success': False,
                'message': 'User created but info retrieval failed'
            }), 500
        
        token = generate_token(user_id)
        
        return jsonify({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user_info['user_id'],
                'username': user_info['username'],
                'email': user_info['email'],
                'full_name': user_info['full_name']
            },
            'token': token
        }), 201
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    try:
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password required'
            }), 400
        
        # Authenticate user
        login_result = UserAuthentication.login_user(username, password)
        
        # Handle tuple response from login_user
        if isinstance(login_result, tuple):
            user_id, message = login_result
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': message
                }), 401
        else:
            user_id = login_result
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': 'Invalid username or password'
                }), 401
        
        user_info = UserAuthentication.get_user_info(user_id)
        
        if not user_info:
            return jsonify({
                'success': False,
                'message': 'User authenticated but info retrieval failed'
            }), 500
        
        token = generate_token(user_id)
        session_manager.set_current_user(user_id, username, user_info['full_name'])
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': {
                'id': user_id,
                'username': user_info['username'],
                'email': user_info['email'],
                'full_name': user_info['full_name']
            },
            'token': token
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/auth/user', methods=['GET'])
@token_required
def get_user(current_user_id):
    """Get current user info"""
    try:
        user_info = UserAuthentication.get_user_info(current_user_id)
        
        if user_info:
            return jsonify({
                'success': True,
                'user': {
                    'id': user_info['user_id'],
                    'username': user_info['username'],
                    'email': user_info['email'],
                    'full_name': user_info['full_name']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============================================================================
# Study Sessions Endpoints
# ============================================================================

@app.route('/api/sessions', methods=['POST'])
@token_required
def add_session(current_user_id):
    """Add new study session"""
    data = request.get_json()

    try:
        subject = data.get('subject', '').strip()
        hours_studied = float(data.get('hours_studied', 0))
        productivity_level = int(data.get('productivity_level', 3))
        notes = data.get('notes', '').strip()
        session_date = data.get('session_date', datetime.now().strftime('%Y-%m-%d'))
        session_time = datetime.now().strftime('%H:%M:%S')  # Always use current time
        
        if not subject or hours_studied <= 0:
            return jsonify({
                'success': False,
                'message': 'Subject and hours are required'
            }), 400
        
        # Add session to database
        result = study_db.add_session(
            current_user_id,
            subject,
            hours_studied,
            productivity_level,
            notes,
            session_date,
            session_time
        )
        
        # Handle tuple response from add_session
        if isinstance(result, tuple):
            success, message = result
            if success:
                # Update subject performance
                subject_db.update_subject_performance(current_user_id, subject, hours_studied, productivity_level)
                
                return jsonify({
                    'success': True,
                    'message': message
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'message': message
                }), 400
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to add session'
            }), 400
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/sessions/today', methods=['GET'])
@token_required
def get_today_sessions(current_user_id):
    """Get today's sessions"""
    try:
        sessions = study_db.get_today_sessions(current_user_id)
        
        if not sessions:
            return jsonify({
                'success': True,
                'sessions': []
            }), 200
        
        return jsonify({
            'success': True,
            'sessions': [
                {
                    'session_id': s[0],
                    'subject': s[1],
                    'hours_studied': s[2],
                    'productivity_level': s[3],
                    'notes': s[4],
                    'session_time': s[5]
                }
                for s in sessions
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/sessions/week', methods=['GET'])
@token_required
def get_week_sessions(current_user_id):
    """Get week's sessions"""
    try:
        sessions = study_db.get_week_sessions(current_user_id)
        
        if not sessions:
            return jsonify({
                'success': True,
                'sessions': []
            }), 200
        
        return jsonify({
            'success': True,
            'sessions': [
                {
                    'subject': s[1],
                    'hours_studied': s[2],
                    'productivity_level': s[3],
                    'session_date': s[0]
                }
                for s in sessions
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/sessions/month', methods=['GET'])
@token_required
def get_month_sessions(current_user_id):
    """Get month's sessions"""
    try:
        sessions = study_db.get_month_sessions(current_user_id)
        
        if not sessions:
            return jsonify({
                'success': True,
                'sessions': []
            }), 200
        
        return jsonify({
            'success': True,
            'sessions': [
                {
                    'session_id': s[0],
                    'session_date': s[1],
                    'subject': s[2],
                    'hours_studied': s[3],
                    'productivity_level': s[4]
                }
                for s in sessions
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/sessions/<int:session_id>', methods=['DELETE'])
@token_required
def delete_session(current_user_id, session_id):
    """Delete a study session"""
    try:
        result = study_db.delete_session(session_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Session deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'Session not found'
            }), 404
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============================================================================
# Reports Endpoints
# ============================================================================

@app.route('/api/reports/weekly', methods=['GET'])
@token_required
def get_weekly_report(current_user_id):
    """Get weekly report"""
    try:
        # User-specific report
        report_generator = WeeklyReportGenerator(current_user_id)
        report = report_generator.generate_report()
        
        if report:
            metrics = report.get('metrics', {})
            patterns = report.get('patterns', {})
            exam_readiness = report.get('exam_readiness', {})
            
            return jsonify({
                'success': True,
                'report': {
                    'total_hours': metrics.get('total_study_hours', 0),
                    'total_sessions': metrics.get('total_sessions', 0),
                    'avg_productivity': metrics.get('avg_productivity', 0),
                    'exam_readiness_score': exam_readiness.get('score', 0),
                    'consistency': patterns.get('consistency', 0),
                    'recommendations': report.get('recommendations', [])
                }
            }), 200
        else:
            return jsonify({
                'success': True,
                'report': None,
                'message': 'No sessions this week'
            }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============================================================================
# Subject Performance Endpoints
# ============================================================================

@app.route('/api/analytics/progress', methods=['GET'])
@token_required
def get_user_progress(current_user_id):
    """Get user progress statistics"""
    try:
        from datetime import datetime, timedelta
        
        # Get this month's sessions
        today = datetime.now()
        month_start = today.replace(day=1)
        
        connection = DatabaseConfig.get_connection()
        cursor = connection.cursor()
        
        # Get this month's stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                SUM(hours_studied) as total_hours,
                AVG(productivity_level) as avg_productivity
            FROM study_sessions
            WHERE user_id = %s AND session_date >= %s
        """, (current_user_id, month_start.strftime("%Y-%m-%d")))
        
        month_stats = cursor.fetchone()
        
        # Get all-time stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_sessions,
                SUM(hours_studied) as total_hours,
                AVG(productivity_level) as avg_productivity
            FROM study_sessions
            WHERE user_id = %s
        """, (current_user_id,))
        
        alltime_stats = cursor.fetchone()
        
        # Calculate daily average for this month
        days_in_month = (today - month_start).days + 1
        month_total_hours = month_stats[1] if month_stats[1] else 0
        daily_average = month_total_hours / days_in_month if days_in_month > 0 else 0
        
        # Get unique subjects this month
        cursor.execute("""
            SELECT COUNT(DISTINCT subject)
            FROM study_sessions
            WHERE user_id = %s AND session_date >= %s
        """, (current_user_id, month_start.strftime("%Y-%m-%d")))
        
        unique_subjects = cursor.fetchone()[0] or 0
        
        cursor.close()
        connection.close()
        
        return jsonify({
            'success': True,
            'progress': {
                'this_month': {
                    'total_hours': round(month_total_hours, 1),
                    'total_sessions': month_stats[0] or 0,
                    'avg_productivity': round(month_stats[2], 1) if month_stats[2] else 0,
                    'daily_average': round(daily_average, 1),
                    'subjects_tracked': unique_subjects
                },
                'all_time': {
                    'total_hours': round(alltime_stats[1], 1) if alltime_stats[1] else 0,
                    'total_sessions': alltime_stats[0] or 0,
                    'avg_productivity': round(alltime_stats[2], 1) if alltime_stats[2] else 0
                }
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/analytics/subjects', methods=['GET'])
@token_required
def get_subject_performance(current_user_id):
    """Get subject performance"""
    try:
        subjects = subject_db.get_subject_performance(current_user_id)
        
        return jsonify({
            'success': True,
            'subjects': [
                {
                    'subject': s[2],
                    'total_hours': s[3],
                    'total_sessions': s[4],
                    'avg_productivity': s[5]
                }
                for s in subjects
            ]
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============================================================================
# Timetable Endpoints
# ============================================================================

@app.route('/api/timetable/latest', methods=['GET'])
@token_required
def get_timetable(current_user_id):
    """Get latest timetable"""
    try:
        timetable = timetable_db.get_latest_timetable(current_user_id)
        
        return jsonify({
            'success': True,
            'timetable': timetable
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/timetable/next-day', methods=['GET'])
@token_required
def get_next_day_timetable(current_user_id):
    """Get recommended timetable for next day"""
    try:
        from timetable_generator import NextDayTimetableGenerator
        
        generator = NextDayTimetableGenerator(current_user_id)
        timetable = generator.generate_next_day_timetable()
        
        return jsonify({
            'success': True,
            'timetable': timetable,
            'recommendations': generator.recommendations
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# ============================================================================
# Health Check Endpoint
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Study Tracker API is running'
    }), 200

# ============================================================================
# Error Handlers
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("STUDY TRACKER - API SERVER")
    print("="*70 + "\n")
    
    print("✓ Flask API Server Starting...")
    print("  API URL: http://localhost:5000/api")
    print("  Frontend: http://localhost:3000")
    print("\n  Endpoints:")
    print("    POST   /api/auth/register      - Register new user")
    print("    POST   /api/auth/login         - Login user")
    print("    GET    /api/auth/user          - Get current user")
    print("    POST   /api/sessions           - Add study session")
    print("    GET    /api/sessions/today     - Get today's sessions")
    print("    GET    /api/sessions/week      - Get week's sessions")
    print("    GET    /api/reports/weekly     - Get weekly report")
    print("    GET    /api/analytics/subjects - Get subject performance")
    print("    GET    /api/health             - Health check")
    print("\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
