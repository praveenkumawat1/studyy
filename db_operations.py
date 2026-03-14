"""
Database Operations Module
Handles all database CRUD operations for study tracker
"""

from datetime import datetime, timedelta
from db_config import DatabaseConfig
import json

class StudySessionDB:
    """Database operations for study sessions"""
    
    @staticmethod
    def add_session(user_id, subject, hours, productivity_level, notes="", session_date=None, session_time=None):
        """Add new study session to database"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False, "Cannot connect to database"
        
        try:
            cursor = connection.cursor()
            
            # Use provided date/time or default to now
            if session_date is None:
                session_date = datetime.now().strftime("%Y-%m-%d")
            if session_time is None:
                session_time = datetime.now().strftime("%H:%M:%S")
            
            cursor.execute("""
                INSERT INTO study_sessions 
                (user_id, subject, hours_studied, productivity_level, notes, session_date, session_time)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (user_id, subject.strip().title(), float(hours), int(productivity_level), notes, session_date, session_time))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, "Session recorded successfully"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def get_today_sessions(user_id):
        """Get all sessions logged today"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            today = datetime.now().strftime("%Y-%m-%d")
            cursor.execute("""
                SELECT session_id, subject, hours_studied, productivity_level, notes, session_time
                FROM study_sessions
                WHERE user_id = %s AND session_date = %s
                ORDER BY session_time
            """, (user_id, today))
            
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            
            sessions = []
            for row in results:
                sessions.append({
                    'session_id': row[0],
                    'subject': row[1],
                    'hours': row[2],
                    'productivity': row[3],
                    'notes': row[4],
                    'time': row[5]
                })
            
            return sessions
        
        except Exception as e:
            print(f"Error getting today's sessions: {e}")
            return None
    
    @staticmethod
    def get_week_sessions(user_id):
        """Get all sessions from this week"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            today = datetime.now()
            week_start = today - timedelta(days=today.weekday())
            
            cursor.execute("""
                SELECT session_date, subject, hours_studied, productivity_level
                FROM study_sessions
                WHERE user_id = %s AND session_date >= %s
                ORDER BY session_date
            """, (user_id, week_start.strftime("%Y-%m-%d")))
            
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            
            return results
        
        except Exception as e:
            print(f"Error getting week sessions: {e}")
            return None
    
    @staticmethod
    def get_month_sessions(user_id):
        """Get all sessions from current month"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            today = datetime.now()
            month_start = today.replace(day=1)
            
            cursor.execute("""
                SELECT session_id, session_date, subject, hours_studied, productivity_level
                FROM study_sessions
                WHERE user_id = %s AND session_date >= %s
                ORDER BY session_date DESC
            """, (user_id, month_start.strftime("%Y-%m-%d")))
            
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            
            return results
        
        except Exception as e:
            print(f"Error getting month sessions: {e}")
            return None
    
    @staticmethod
    def delete_session(user_id, session_id):
        """Delete a study session"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            cursor.execute("""
                DELETE FROM study_sessions
                WHERE session_id = %s AND user_id = %s
            """, (session_id, user_id))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

class SubjectPerformanceDB:
    """Database operations for subject performance"""
    
    @staticmethod
    def update_subject_performance(user_id, subject, hours, productivity):
        """Update or create subject performance record"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Check if subject exists
            cursor.execute("""
                SELECT performance_id FROM subject_performance
                WHERE user_id = %s AND subject = %s
            """, (user_id, subject))
            
            result = cursor.fetchone()
            
            if result:
                # Update existing
                cursor.execute("""
                    UPDATE subject_performance
                    SET total_hours = total_hours + %s,
                        total_sessions = total_sessions + 1,
                        avg_productivity = (avg_productivity * total_sessions + %s) / (total_sessions + 1),
                        last_session_date = %s
                    WHERE user_id = %s AND subject = %s
                """, (hours, productivity, datetime.now().strftime("%Y-%m-%d"), user_id, subject))
            else:
                # Insert new
                cursor.execute("""
                    INSERT INTO subject_performance
                    (user_id, subject, total_hours, total_sessions, avg_productivity, last_session_date, first_session_date)
                    VALUES (%s, %s, %s, 1, %s, %s, %s)
                """, (user_id, subject, hours, productivity, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%Y-%m-%d")))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        
        except Exception as e:
            print(f"Error updating subject performance: {e}")
            return False
    
    @staticmethod
    def get_subject_performance(user_id):
        """Get all subject performance data"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT subject, total_hours, total_sessions, avg_productivity, last_session_date
                FROM subject_performance
                WHERE user_id = %s
                ORDER BY total_hours DESC
            """, (user_id,))
            
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            
            performance = {}
            for row in results:
                performance[row[0]] = {
                    'hours': row[1],
                    'sessions': row[2],
                    'avg_productivity': row[3],
                    'last_session': row[4]
                }
            
            return performance
        
        except Exception as e:
            print(f"Error getting subject performance: {e}")
            return None

class WeeklyReportDB:
    """Database operations for weekly reports"""
    
    @staticmethod
    def save_report(user_id, week_start, week_end, total_hours, total_sessions, avg_productivity, exam_readiness_score, recommendations):
        """Save weekly report to database"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Convert recommendations list to JSON
            rec_json = json.dumps(recommendations) if isinstance(recommendations, list) else recommendations
            
            cursor.execute("""
                INSERT INTO weekly_reports
                (user_id, week_start, week_end, total_hours, total_sessions, avg_productivity, exam_readiness_score, recommendations)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, week_start, week_end, total_hours, total_sessions, avg_productivity, exam_readiness_score, rec_json))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        
        except Exception as e:
            print(f"Error saving report: {e}")
            return False
    
    @staticmethod
    def get_latest_report(user_id):
        """Get latest weekly report"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT week_start, week_end, total_hours, total_sessions, avg_productivity, exam_readiness_score, recommendations
                FROM weekly_reports
                WHERE user_id = %s
                ORDER BY week_start DESC
                LIMIT 1
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                recommendations = json.loads(result[6]) if result[6] else []
                return {
                    'week_start': result[0],
                    'week_end': result[1],
                    'total_hours': result[2],
                    'total_sessions': result[3],
                    'avg_productivity': result[4],
                    'exam_readiness_score': result[5],
                    'recommendations': recommendations
                }
            
            return None
        
        except Exception as e:
            print(f"Error getting report: {e}")
            return None
    
    @staticmethod
    def get_reports_history(user_id, weeks=4):
        """Get report history"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT week_start, week_end, total_hours, exam_readiness_score
                FROM weekly_reports
                WHERE user_id = %s
                ORDER BY week_start DESC
                LIMIT %s
            """, (user_id, weeks))
            
            results = cursor.fetchall()
            cursor.close()
            connection.close()
            
            return results
        
        except Exception as e:
            print(f"Error getting report history: {e}")
            return None

class TimetableDB:
    """Database operations for timetables"""
    
    @staticmethod
    def save_timetable(user_id, week_start, timetable_data):
        """Save generated timetable"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            
            # Convert timetable to JSON
            timetable_json = json.dumps(timetable_data)
            
            cursor.execute("""
                INSERT INTO timetables
                (user_id, week_start, timetable_data)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE
                timetable_data = %s,
                created_at = CURRENT_TIMESTAMP
            """, (user_id, week_start, timetable_json, timetable_json))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True
        
        except Exception as e:
            print(f"Error saving timetable: {e}")
            return False
    
    @staticmethod
    def get_latest_timetable(user_id):
        """Get latest timetable"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT timetable_data, week_start
                FROM timetables
                WHERE user_id = %s
                ORDER BY week_start DESC
                LIMIT 1
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                return {
                    'timetable': json.loads(result[0]),
                    'week_start': result[1]
                }
            
            return None
        
        except Exception as e:
            print(f"Error getting timetable: {e}")
            return None

if __name__ == "__main__":
    print("Database operations module loaded successfully")
