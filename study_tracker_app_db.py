"""
Study Tracker with MySQL Database Integration
Main Application with User Authentication
"""

import os
import sys
from datetime import datetime
from auth import UserAuthentication, SessionManager, session
from db_operations import StudySessionDB, SubjectPerformanceDB, WeeklyReportDB, TimetableDB
from daily_tracker import DailyStudyTracker
from weekly_report import WeeklyReportGenerator
from timetable_generator import TimetableGenerator

class StudyTrackerDBApp:
    """Main application with database integration"""
    
    def __init__(self):
        self.session = session
        self.running = True
    
    def clear_screen(self):
        """Clear console"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_login_menu(self):
        """Display login/register menu"""
        self.clear_screen()
        print("\n" + "="*80)
        print("AI-BASED STUDY TRACKER - USER AUTHENTICATION")
        print("="*80)
        print("\n" + " "*20 + "Welcome to Study Tracker!\n")
        print("-"*80)
        print("\n1. 📝 REGISTER - Create new account")
        print("2. 🔓 LOGIN - Sign into existing account")
        print("3. 🚪 EXIT - Quit application")
        print("\n" + "-"*80)
    
    def register_user(self):
        """Register new user"""
        print("\n" + "="*80)
        print("USER REGISTRATION")
        print("="*80 + "\n")
        
        while True:
            username = input("Username (3-50 characters): ").strip()
            if len(username) < 3:
                print("❌ Username must be at least 3 characters\n")
                continue
            break
        
        while True:
            email = input("Email: ").strip()
            if "@" not in email:
                print("❌ Invalid email format\n")
                continue
            break
        
        while True:
            password = input("Password (min 6 chars, must have uppercase, lowercase, number): ")
            valid, msg = UserAuthentication.is_valid_password(password)
            if not valid:
                print(f"❌ {msg}\n")
                continue
            break
        
        confirm_password = input("Confirm Password: ")
        
        if password != confirm_password:
            print("❌ Passwords do not match!\n")
            input("Press Enter to continue...")
            return False
        
        full_name = input("Full Name: ").strip()
        
        success, message = UserAuthentication.register_user(username, email, password, full_name)
        
        if success:
            print(f"\n✓ {message}")
            print("You can now login with your credentials")
        else:
            print(f"\n❌ {message}")
        
        input("\nPress Enter to continue...")
        return success
    
    def login_user(self):
        """Login user"""
        print("\n" + "="*80)
        print("USER LOGIN")
        print("="*80 + "\n")
        
        username = input("Username: ").strip()
        password = input("Password: ")
        
        if self.session.login(username, password):
            return True
        
        input("\nPress Enter to continue...")
        return False
    
    def display_main_menu(self):
        """Display main menu"""
        self.clear_screen()
        
        print("\n" + "="*80)
        print("AI-BASED STUDY TRACKER & EXAM READINESS ANALYZER")
        print("="*80)
        
        user_info = self.session.current_full_name
        print(f"\n            Welcome, {user_info}!")
        print("        Intelligent Study Planning & Progress Monitoring\n")
        print("-"*80)
        print("\n1. 📝 DAILY TRACKING")
        print("   └─ Log study sessions, subjects, and hours")
        print("\n2. 📊 WEEKLY REPORT")
        print("   └─ View performance analysis & exam readiness")
        print("\n3. 📅 GENERATE STUDY TIMETABLE")
        print("   └─ Get AI-optimized weekly study schedule")
        print("\n4. 🎯 SUBJECT RECOMMENDATIONS")
        print("   └─ Get personalized study suggestions")
        print("\n5. 📈 VIEW PROGRESS")
        print("   └─ Check daily/weekly summaries")
        print("\n6. ⚙️  ACCOUNT SETTINGS")
        print("   └─ Change password, view profile")
        print("\n7. 🚪 LOGOUT")
        print("\n" + "-"*80)
    
    def run_daily_tracker(self):
        """Run daily tracking with database"""
        print("\n" + "="*80)
        print("DAILY STUDY TRACKING")
        print("="*80 + "\n")
        
        user_id = self.session.get_user_id()
        
        # Get today's sessions from database
        today_sessions = StudySessionDB.get_today_sessions(user_id)
        
        if today_sessions:
            print(f"✓ Sessions already logged today: {len(today_sessions)}")
            total_hours = sum(s['hours'] for s in today_sessions)
            print(f"  Total Hours: {total_hours:.2f}\n")
        
        print("1. Add new study session")
        print("2. View today's summary")
        print("3. View this week's summary")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            print("\n" + "-"*80)
            print("ADD NEW STUDY SESSION")
            print("-"*80 + "\n")
            
            subject = input("Subject name: ").strip()
            
            try:
                hours = float(input("Hours studied: "))
            except ValueError:
                print("❌ Invalid input")
                input("Press Enter to continue...")
                return
            
            print("\nProductivity Level (1=Poor, 5=Excellent):")
            try:
                productivity = int(input("Rating (1-5): "))
                if productivity < 1 or productivity > 5:
                    raise ValueError
            except ValueError:
                print("❌ Invalid rating")
                input("Press Enter to continue...")
                return
            
            notes = input("Notes (optional): ").strip()
            
            # Save to database
            success, message = StudySessionDB.add_session(
                user_id, subject, hours, productivity, notes
            )
            
            if success:
                # Update subject performance
                SubjectPerformanceDB.update_subject_performance(user_id, subject, hours, productivity)
                print(f"✓ {message}")
            else:
                print(f"❌ {message}")
            
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            print("\n" + "="*80)
            print("TODAY'S SUMMARY")
            print("="*80)
            
            today_sessions = StudySessionDB.get_today_sessions(user_id)
            
            if today_sessions:
                total_hours = sum(s['hours'] for s in today_sessions)
                avg_productivity = sum(s['productivity'] for s in today_sessions) / len(today_sessions)
                
                print(f"\nDate: {datetime.now().strftime('%Y-%m-%d')}")
                print(f"Total Hours: {total_hours:.2f}")
                print(f"Sessions: {len(today_sessions)}")
                print(f"Average Productivity: {avg_productivity:.2f}/5\n")
                
                print("Session Details:")
                for i, sess in enumerate(today_sessions, 1):
                    print(f"  {i}. {sess['subject']:20} {sess['hours']:5.1f}h (Productivity: {sess['productivity']}/5)")
            else:
                print("\nNo sessions logged today.")
            
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            print("\n" + "="*80)
            print("WEEKLY SUMMARY")
            print("="*80)
            
            week_sessions = StudySessionDB.get_week_sessions(user_id)
            
            if week_sessions:
                total_hours = sum(s[2] for s in week_sessions)
                total_sessions = len(week_sessions)
                avg_productivity = sum(s[3] for s in week_sessions) / len(week_sessions) if week_sessions else 0
                
                print(f"\nTotal Hours: {total_hours:.2f}")
                print(f"Total Sessions: {total_sessions}")
                print(f"Average Productivity: {avg_productivity:.2f}/5")
            else:
                print("\nNo sessions logged this week.")
            
            input("\nPress Enter to continue...")
    
    def run_weekly_report(self):
        """Generate and display weekly report"""
        print("\n" + "="*80)
        print("GENERATING WEEKLY REPORT")
        print("="*80)
        
        user_id = self.session.get_user_id()
        
        # Get data from database
        week_sessions = StudySessionDB.get_week_sessions(user_id)
        subject_perf = SubjectPerformanceDB.get_subject_performance(user_id)
        
        if not week_sessions:
            print("\n❌ No sessions logged this week")
            input("Press Enter to continue...")
            return
        
        # Calculate metrics
        total_hours = sum(s[2] for s in week_sessions)
        total_sessions = len(week_sessions)
        avg_productivity = sum(s[3] for s in week_sessions) / len(week_sessions)
        
        # Calculate exam readiness
        readiness_score = min(100, int(
            (total_hours / 20 * 30) +
            (avg_productivity / 5 * 30) +
            (len(set(s[1] for s in week_sessions)) / 5 * 20) +
            20
        ))
        
        print(f"\n{'─'*80}")
        print("WEEKLY SUMMARY")
        print(f"{'─'*80}")
        print(f"Total Hours: {total_hours:.2f}")
        print(f"Sessions: {total_sessions}")
        print(f"Average Productivity: {avg_productivity:.2f}/5")
        print(f"\nExam Readiness Score: {readiness_score}/100")
        
        if readiness_score >= 80:
            status = "EXCELLENT"
        elif readiness_score >= 65:
            status = "GOOD"
        elif readiness_score >= 50:
            status = "MODERATE"
        else:
            status = "NEEDS IMPROVEMENT"
        
        print(f"Status: {status}")
        
        # Show subject performance
        if subject_perf:
            print(f"\n{'─'*80}")
            print("SUBJECT PERFORMANCE")
            print(f"{'─'*80}")
            for subject, data in subject_perf.items():
                print(f"\n{subject}:")
                print(f"  Hours: {data['hours']:.2f}")
                print(f"  Sessions: {data['sessions']}")
                print(f"  Avg Productivity: {data['avg_productivity']:.2f}/5")
        
        # Save report
        print(f"\n{'─'*80}")
        save = input("Save report to database? (y/n): ").strip().lower()
        if save == 'y':
            recommendations = ["Stay consistent", "Focus on weak areas"]
            WeeklyReportDB.save_report(
                user_id,
                datetime.now().date(),
                datetime.now().date(),
                total_hours,
                total_sessions,
                avg_productivity,
                readiness_score,
                recommendations
            )
            print("✓ Report saved")
        
        input("\nPress Enter to continue...")
    
    def view_progress(self):
        """View progress and statistics"""
        print("\n" + "="*80)
        print("YOUR PROGRESS & STATISTICS")
        print("="*80 + "\n")
        
        user_id = self.session.get_user_id()
        
        # Month sessions
        month_sessions = StudySessionDB.get_month_sessions(user_id)
        
        if month_sessions:
            total_hours = sum(s[3] for s in month_sessions)
            total_sessions = len(month_sessions)
            
            print("CURRENT MONTH STATISTICS:")
            print("-" * 80)
            print(f"Total Study Hours: {total_hours:.2f}")
            print(f"Total Sessions: {total_sessions}")
            print(f"Average Session: {total_hours/total_sessions if total_sessions > 0 else 0:.2f} hours")
            
            # Subject performance
            subject_perf = SubjectPerformanceDB.get_subject_performance(user_id)
            if subject_perf:
                print("\nSUBJECT PERFORMANCE:")
                print("-" * 80)
                for subject, data in subject_perf.items():
                    print(f"{subject:20} {data['hours']:7.2f}h  {data['sessions']:3} sessions  Avg: {data['avg_productivity']:.2f}/5")
        else:
            print("No data available. Start logging sessions!")
        
        input("\nPress Enter to continue...")
    
    def account_settings(self):
        """User account settings"""
        print("\n" + "="*80)
        print("ACCOUNT SETTINGS")
        print("="*80 + "\n")
        
        print("1. Change Password")
        print("2. View Profile")
        print("3. Delete Account")
        print("4. Back to Menu")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        user_id = self.session.get_user_id()
        
        if choice == '1':
            print("\nCHANGE PASSWORD")
            old_password = input("Current Password: ")
            new_password = input("New Password: ")
            confirm = input("Confirm Password: ")
            
            if new_password != confirm:
                print("❌ Passwords don't match")
            else:
                success, msg = UserAuthentication.change_password(user_id, old_password, new_password)
                print(f"{'✓' if success else '❌'} {msg}")
        
        elif choice == '2':
            print("\nUSER PROFILE")
            user_info = UserAuthentication.get_user_info(user_id)
            if user_info:
                print(f"Username: {user_info['username']}")
                print(f"Email: {user_info['email']}")
                print(f"Full Name: {user_info['full_name']}")
                print(f"Joined: {user_info['created_at']}")
                if user_info['last_login']:
                    print(f"Last Login: {user_info['last_login']}")
        
        elif choice == '3':
            confirm = input("Type 'DELETE' to confirm account deletion: ").strip()
            if confirm == 'DELETE':
                success, msg = UserAuthentication.delete_account(user_id)
                if success:
                    print("✓ Account deleted")
                    self.session.logout()
                    return
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main application loop"""
        while self.running:
            if not self.session.is_logged_in():
                # Auth loop
                self.display_login_menu()
                choice = input("\nEnter choice (1-3): ").strip()
                
                if choice == '1':
                    self.register_user()
                elif choice == '2':
                    if self.login_user():
                        pass
                elif choice == '3':
                    print("\nThank you for using Study Tracker!")
                    self.running = False
            
            else:
                # Main app loop
                self.display_main_menu()
                choice = input("\nEnter your choice (1-7): ").strip()
                
                if choice == '1':
                    self.run_daily_tracker()
                elif choice == '2':
                    self.run_weekly_report()
                elif choice == '3':
                    print("\n✓ Timetable generation (non-DB version still available)")
                    input("Press Enter to continue...")
                elif choice == '4':
                    print("\n✓ Recommendations (non-DB version still available)")
                    input("Press Enter to continue...")
                elif choice == '5':
                    self.view_progress()
                elif choice == '6':
                    self.account_settings()
                elif choice == '7':
                    self.session.logout()
                    print("Goodbye! 👋\n")

def main():
    """Entry point"""
    try:
        app = StudyTrackerDBApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication terminated by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("  1. MySQL server is running")
        print("  2. Database is initialized (run setup_database.py)")
        print("  3. Check db_config.py for connection settings")

if __name__ == "__main__":
    main()
