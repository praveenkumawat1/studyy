"""
MySQL Database Configuration
Handles database connection and setup
"""

import mysql.connector
from mysql.connector import Error
import os

class DatabaseConfig:
    """Database connection configuration"""
    
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',
        'database': 'study_tracker_db',
        'port': 3306
    }
    
    @staticmethod
    def get_connection():
        """Get MySQL database connection"""
        try:
            connection = mysql.connector.connect(**DatabaseConfig.DB_CONFIG)
            if connection.is_connected():
                return connection
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
    
    @staticmethod
    def test_connection():
        """Test database connection"""
        connection = DatabaseConfig.get_connection()
        if connection:
            print("✓ Database connection successful")
            connection.close()
            return True
        else:
            print("❌ Database connection failed")
            return False

class DatabaseSetup:
    """Initialize database and create tables"""
    
    @staticmethod
    def create_database():
        """Create the study tracker database"""
        try:
            connection = mysql.connector.connect(
                host=DatabaseConfig.DB_CONFIG['host'],
                user=DatabaseConfig.DB_CONFIG['user'],
                password=DatabaseConfig.DB_CONFIG['password'],
                port=DatabaseConfig.DB_CONFIG['port']
            )
            
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DatabaseConfig.DB_CONFIG['database']}")
            print("✓ Database created successfully")
            cursor.close()
            connection.close()
            return True
        
        except Error as e:
            print(f"Error creating database: {e}")
            return False
    
    @staticmethod
    def create_tables():
        """Create all required tables"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            print("Cannot connect to database")
            return False
        
        cursor = connection.cursor()
        
        try:
            # Users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    full_name VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP NULL,
                    is_active BOOLEAN DEFAULT TRUE
                )
            """)
            print("✓ Users table created")
            
            # Study Sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS study_sessions (
                    session_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    hours_studied FLOAT NOT NULL,
                    productivity_level INT CHECK (productivity_level >= 1 AND productivity_level <= 5),
                    notes TEXT,
                    session_date DATE NOT NULL,
                    session_time TIME NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_user_date (user_id, session_date)
                )
            """)
            print("✓ Study Sessions table created")
            
            # Weekly Reports table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weekly_reports (
                    report_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    week_start DATE NOT NULL,
                    week_end DATE NOT NULL,
                    total_hours FLOAT,
                    total_sessions INT,
                    avg_productivity FLOAT,
                    exam_readiness_score INT,
                    recommendations TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_user_week (user_id, week_start)
                )
            """)
            print("✓ Weekly Reports table created")
            
            # Timetables table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS timetables (
                    timetable_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    week_start DATE NOT NULL,
                    timetable_data LONGTEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    INDEX idx_user_week (user_id, week_start)
                )
            """)
            print("✓ Timetables table created")
            
            # Subject Performance table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subject_performance (
                    performance_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    total_hours FLOAT,
                    total_sessions INT,
                    avg_productivity FLOAT,
                    last_session_date DATE,
                    first_session_date DATE,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                    UNIQUE KEY unique_user_subject (user_id, subject)
                )
            """)
            print("✓ Subject Performance table created")
            
            # Goals table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goals (
                    goal_id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    subject VARCHAR(100) NOT NULL,
                    target_hours FLOAT,
                    target_sessions INT,
                    deadline DATE,
                    achieved BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
                )
            """)
            print("✓ Goals table created")
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print("\n✓ All tables created successfully!")
            return True
        
        except Error as e:
            print(f"Error creating tables: {e}")
            connection.rollback()
            return False
    
    @staticmethod
    def initialize_database():
        """Initialize complete database"""
        print("\n" + "="*60)
        print("INITIALIZING DATABASE")
        print("="*60 + "\n")
        
        if DatabaseSetup.create_database():
            if DatabaseSetup.create_tables():
                print("\n✓ DATABASE INITIALIZATION COMPLETE!")
                return True
        
        return False

if __name__ == "__main__":
    # Test connection
    print("Testing database configuration...")
    DatabaseConfig.test_connection()
    
    # Initialize database
    DatabaseSetup.initialize_database()
