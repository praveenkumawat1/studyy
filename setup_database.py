"""
Database Setup & Installation Script
Initializes MySQL database for Study Tracker
"""

import sys
from db_config import DatabaseConfig, DatabaseSetup

def install_mysql():
    """Guide user to install MySQL if needed"""
    print("\n" + "="*70)
    print("MYSQL INSTALLATION GUIDE")
    print("="*70 + "\n")
    
    print("If MySQL is not installed, follow these steps:\n")
    
    print("WINDOWS:")
    print("  1. Download MySQL from: https://dev.mysql.com/downloads/mysql/")
    print("  2. Run the installer")
    print("  3. Choose 'Developer Default' setup")
    print("  4. Configure MySQL Server on startup")
    print("  5. Note: Default user 'root' with no password")
    print("  6. Open MySQL Command Line Client and run:")
    print("     mysql -u root")
    
    print("\nLINUX (Ubuntu/Debian):")
    print("  1. Open terminal and run:")
    print("     sudo apt-get install mysql-server")
    print("  2. Start MySQL: sudo systemctl start mysql")
    print("  3. Secure installation: sudo mysql_secure_installation")
    
    print("\nMAC:")
    print("  1. Install via Homebrew: brew install mysql")
    print("  2. Start service: brew services start mysql")
    print("  3. Secure: mysql_secure_installation")

def install_python_packages():
    """Install required Python packages"""
    print("\n" + "="*70)
    print("INSTALLING PYTHON PACKAGES")
    print("="*70 + "\n")
    
    packages = ['mysql-connector-python', 'pandas', 'scikit-learn', 'numpy', 'joblib']
    
    print("Installing required packages...")
    print(f"Packages to install: {', '.join(packages)}\n")
    
    import subprocess
    for package in packages:
        try:
            print(f"Installing {package}...", end=" ")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print("✓")
        except subprocess.CalledProcessError:
            print(f"✗ Failed to install {package}")
            return False
    
    print("\n✓ All packages installed successfully!")
    return True

def setup_database():
    """Setup database"""
    print("\n" + "="*70)
    print("DATABASE SETUP")
    print("="*70 + "\n")
    
    print("Initializing database...")
    if DatabaseSetup.initialize_database():
        return True
    else:
        print("❌ Database initialization failed")
        return False

def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("STUDY TRACKER - DATABASE INSTALLATION")
    print("="*70 + "\n")
    
    print("This script will:")
    print("  1. Check MySQL installation")
    print("  2. Install required Python packages")
    print("  3. Create the study_tracker_db database")
    print("  4. Create all required tables\n")
    
    # Check MySQL
    print("Step 1: Checking MySQL installation...")
    try:
        import mysql.connector
        test_conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            port=3306
        )
        test_conn.close()
        print("✓ MySQL is installed and running\n")
    except Exception as e:
        print(f"\n⚠️  MySQL connection failed: {e}\n")
        response = input("Do you want installation instructions? (y/n): ").strip().lower()
        if response == 'y':
            install_mysql()
        return False
    
    # Install Python packages
    print("Step 2: Installing Python packages...")
    if not install_python_packages():
        print("❌ Package installation failed")
        return False
    
    # Setup database
    print("\nStep 3: Setting up database...")
    if not setup_database():
        print("❌ Database setup failed")
        return False
    
    # Success
    print("\n" + "="*70)
    print("✓ INSTALLATION COMPLETE!")
    print("="*70 + "\n")
    
    print("Next steps:")
    print("  1. Run: python study_tracker_app_db.py")
    print("  2. Register a new account")
    print("  3. Start tracking your study!")
    print("\nDatabase Details:")
    print("  Database Name: study_tracker_db")
    print("  Host: localhost")
    print("  Port: 3306")
    print("  User: root")
    
    print("\n✓ You're all set! Happy studying! 📚\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
