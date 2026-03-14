"""
User Authentication Module
Handles user registration, login, and session management
"""

import hashlib
import secrets
import re
from datetime import datetime
from db_config import DatabaseConfig

class PasswordHasher:
    """Secure password hashing"""
    
    @staticmethod
    def hash_password(password):
        """Hash password with salt"""
        salt = secrets.token_hex(32)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${password_hash.hex()}"
    
    @staticmethod
    def verify_password(password, hashed):
        """Verify password against hash"""
        try:
            salt, hash_value = hashed.split('$')
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash.hex() == hash_value
        except:
            return False

class UserAuthentication:
    """User authentication and management"""
    
    @staticmethod
    def is_valid_email(email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def is_valid_username(username):
        """Validate username format"""
        if len(username) < 3 or len(username) > 50:
            return False
        return re.match(r'^[a-zA-Z0-9_-]+$', username) is not None
    
    @staticmethod
    def is_valid_password(password):
        """Validate password strength"""
        if len(password) < 6:
            return False, "Password must be at least 6 characters"
        if not re.search(r'[a-z]', password):
            return False, "Password must contain lowercase letters"
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain uppercase letters"
        if not re.search(r'[0-9]', password):
            return False, "Password must contain numbers"
        return True, "Valid password"
    
    @staticmethod
    def register_user(username, email, password, full_name):
        """Register new user"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False, "Cannot connect to database"
        
        # Validation
        if not UserAuthentication.is_valid_username(username):
            return False, "Invalid username (3-50 alphanumeric characters, _ or -)"
        
        if not UserAuthentication.is_valid_email(email):
            return False, "Invalid email format"
        
        valid, msg = UserAuthentication.is_valid_password(password)
        if not valid:
            return False, msg
        
        try:
            cursor = connection.cursor()
            
            # Check if username/email exists
            cursor.execute("SELECT user_id FROM users WHERE username = %s OR email = %s", 
                          (username, email))
            if cursor.fetchone():
                return False, "Username or email already exists"
            
            # Hash password
            hashed_password = PasswordHasher.hash_password(password)
            
            # Insert user
            cursor.execute("""
                INSERT INTO users (username, email, password, full_name)
                VALUES (%s, %s, %s, %s)
            """, (username, email, hashed_password, full_name))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print(f"✓ User '{username}' registered successfully!")
            return True, "Registration successful"
        
        except Exception as e:
            print(f"❌ Registration error: {e}")
            return False, f"Registration error: {str(e)}"
    
    @staticmethod
    def login_user(username, password):
        """Login user"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None, "Cannot connect to database"
        
        try:
            cursor = connection.cursor()
            
            # Get user
            cursor.execute("""
                SELECT user_id, password, full_name, is_active 
                FROM users 
                WHERE username = %s
            """, (username,))
            
            result = cursor.fetchone()
            
            if not result:
                return None, "Username not found"
            
            user_id, hashed_password, full_name, is_active = result
            
            if not is_active:
                return None, "Account is deactivated"
            
            # Verify password
            if not PasswordHasher.verify_password(password, hashed_password):
                return None, "Invalid password"
            
            # Update last login
            cursor.execute("""
                UPDATE users 
                SET last_login = %s 
                WHERE user_id = %s
            """, (datetime.now(), user_id))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            print(f"✓ Welcome back, {full_name}!")
            return user_id, "Login successful"
        
        except Exception as e:
            print(f"❌ Login error: {e}")
            return None, f"Login error: {str(e)}"
    
    @staticmethod
    def get_user_info(user_id):
        """Get user information"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            
            cursor.execute("""
                SELECT user_id, username, email, full_name, created_at, last_login
                FROM users
                WHERE user_id = %s
            """, (user_id,))
            
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if result:
                return {
                    'user_id': result[0],
                    'username': result[1],
                    'email': result[2],
                    'full_name': result[3],
                    'created_at': result[4],
                    'last_login': result[5]
                }
            return None
        
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change user password"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False, "Cannot connect to database"
        
        try:
            cursor = connection.cursor()
            
            # Get current password
            cursor.execute("SELECT password FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            
            if not result:
                return False, "User not found"
            
            # Verify old password
            if not PasswordHasher.verify_password(old_password, result[0]):
                return False, "Old password is incorrect"
            
            # Validate new password
            valid, msg = UserAuthentication.is_valid_password(new_password)
            if not valid:
                return False, msg
            
            # Update password
            hashed_password = PasswordHasher.hash_password(new_password)
            cursor.execute("""
                UPDATE users 
                SET password = %s 
                WHERE user_id = %s
            """, (hashed_password, user_id))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, "Password changed successfully"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    @staticmethod
    def delete_account(user_id):
        """Delete user account"""
        connection = DatabaseConfig.get_connection()
        
        if not connection:
            return False, "Cannot connect to database"
        
        try:
            cursor = connection.cursor()
            
            # Delete user (cascading deletes will remove related data)
            cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            
            connection.commit()
            cursor.close()
            connection.close()
            
            return True, "Account deleted successfully"
        
        except Exception as e:
            return False, f"Error: {str(e)}"

class SessionManager:
    """Manage user sessions"""
    
    def __init__(self):
        self.current_user_id = None
        self.current_username = None
        self.current_full_name = None
    
    def login(self, username, password):
        """Login user"""
        user_id, message = UserAuthentication.login_user(username, password)
        
        if user_id:
            self.current_user_id = user_id
            self.current_username = username
            
            user_info = UserAuthentication.get_user_info(user_id)
            if user_info:
                self.current_full_name = user_info['full_name']
            
            return True
        else:
            print(f"❌ {message}")
            return False
    
    def logout(self):
        """Logout user"""
        self.current_user_id = None
        self.current_username = None
        self.current_full_name = None
        print("✓ Logged out successfully")
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.current_user_id is not None
    
    def get_user_id(self):
        """Get current user ID"""
        return self.current_user_id
    
    def get_username(self):
        """Get current username"""
        return self.current_username
    
    def get_full_name(self):
        """Get current user's full name"""
        return self.current_full_name

# Global session manager
session = SessionManager()

if __name__ == "__main__":
    print("Testing authentication module...\n")
    
    # Test registration
    print("1. Testing registration")
    success, msg = UserAuthentication.register_user(
        "testuser",
        "test@example.com",
        "TestPass123",
        "Test User"
    )
    print(f"   {msg}\n")
    
    # Test login
    print("2. Testing login")
    user_id, msg = UserAuthentication.login_user("testuser", "TestPass123")
    print(f"   {msg}\n")
    
    # Test get user info
    if user_id:
        print("3. Getting user info")
        user_info = UserAuthentication.get_user_info(user_id)
        if user_info:
            print(f"   Username: {user_info['username']}")
            print(f"   Email: {user_info['email']}")
            print(f"   Full Name: {user_info['full_name']}")
