"""
AI-Based Study Tracker - Main Application
Integrates all modules for complete study tracking and analysis
"""

import os
import sys
from datetime import datetime
from daily_tracker import DailyStudyTracker
from weekly_report import WeeklyReportGenerator
from timetable_generator import TimetableGenerator

class StudyTrackerApp:
    def __init__(self):
        self.tracker = DailyStudyTracker()
        self.weekly_report = WeeklyReportGenerator(self.tracker)
        self.timetable_gen = TimetableGenerator(self.weekly_report)
        self.running = True
    
    def clear_screen(self):
        """Clear console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_main_menu(self):
        """Display main menu"""
        self.clear_screen()
        print("\n" + "="*80)
        print("AI-BASED STUDY TRACKER & EXAM READINESS ANALYZER")
        print("="*80)
        print("\n              Intelligent Study Planning & Progress Monitoring\n")
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
        print("\n6. ❓ HELP & GUIDE")
        print("   └─ Learn about the system features")
        print("\n7. 🚪 EXIT")
        print("\n" + "-"*80)
    
    def run_daily_tracker(self):
        """Run daily tracking module"""
        print("\n" + "="*80)
        print("DAILY STUDY TRACKING")
        print("="*80 + "\n")
        
        today_summary = self.tracker.get_today_summary()
        existing_sessions = 0
        
        if today_summary:
            existing_sessions = today_summary['sessions']
            print(f"✓ Sessions already logged today: {existing_sessions}")
            print(f"  Total Hours: {today_summary['total_hours']:.2f}")
            print(f"  Subjects: {', '.join(today_summary['subjects'])}\n")
        
        print("1. Add new study session")
        print("2. View today's summary")
        print("3. View this week's summary")
        print("4. Back to main menu")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            self.tracker.log_daily_sessions()
            input("\nPress Enter to continue...")
        
        elif choice == '2':
            summary = self.tracker.get_today_summary()
            if summary:
                print("\n" + "="*80)
                print("TODAY'S STUDY SUMMARY")
                print("="*80)
                print(f"Date: {summary['date']}")
                print(f"Total Hours: {summary['total_hours']:.2f}")
                print(f"Sessions: {summary['sessions']}")
                print(f"Subjects: {', '.join(summary['subjects'])}")
                print(f"Average Productivity: {summary['avg_productivity']:.2f}/5")
                print("\nSession Details:")
                for i, sess in enumerate(summary['sessions_detail'], 1):
                    print(f"  {i}. {sess['subject']:20} {sess['hours_studied']:5.1f}h (Productivity: {sess['productivity_level']}/5)")
            else:
                print("\n❌ No sessions logged today.")
            
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            summary = self.tracker.get_week_summary()
            if summary:
                print("\n" + "="*80)
                print("WEEKLY STUDY SUMMARY")
                print("="*80)
                print(f"Week: {summary['week_start']} to {summary['week_end']}")
                print(f"Total Hours: {summary['total_hours']:.2f}")
                print(f"Total Sessions: {summary['total_sessions']}")
                print(f"Average Productivity: {summary['avg_productivity']:.2f}/5")
                
                print("\nDaily Breakdown:")
                for date, data in sorted(summary['daily_breakdown'].items()):
                    print(f"  {date}: {data['hours']:5.1f}h ({data['sessions']} sessions, "
                          f"Productivity: {data['avg_productivity']:.2f}/5)")
            else:
                print("\n❌ No sessions logged this week.")
            
            input("\nPress Enter to continue...")
    
    def run_weekly_report(self):
        """Run weekly report generation"""
        print("\n" + "="*80)
        print("Generating Weekly Report...")
        print("="*80)
        
        self.weekly_report.generate_report()
        
        # Save option
        save = input("\nSave report to file? (y/n): ").strip().lower()
        if save == 'y':
            self.weekly_report.save_report()
        
        input("\nPress Enter to continue...")
    
    def run_timetable_generator(self):
        """Run timetable generator"""
        print("\n" + "="*80)
        print("Generating Your Personalized Study Plan...")
        print("="*80)
        
        # Check if weekly report has data
        if not self.weekly_report.report:
            print("\nGenerating analysis from your study data...")
            self.weekly_report.generate_report()
        
        self.timetable_gen.generate_full_plan()
        
        # Save option
        save = input("\nSave timetable to file? (y/n): ").strip().lower()
        if save == 'y':
            self.timetable_gen.save_timetable()
        
        input("\nPress Enter to continue...")
    
    def show_recommendations(self):
        """Show subject recommendations"""
        print("\n" + "="*80)
        print("SUBJECT-SPECIFIC RECOMMENDATIONS")
        print("="*80)
        
        # Ensure weekly report is ready
        if not self.weekly_report.report:
            print("\nAnalyzing your study data...")
            self.weekly_report.generate_report()
        
        self.timetable_gen.analyze_subject_priorities()
        self.timetable_gen.get_subject_recommendations()
        
        input("\nPress Enter to continue...")
    
    def show_progress(self):
        """Show progress and statistics"""
        print("\n" + "="*80)
        print("YOUR PROGRESS & STATISTICS")
        print("="*80 + "\n")
        
        # Subject performance
        perf = self.tracker.get_subject_performance()
        if perf:
            print("SUBJECT PERFORMANCE:")
            print("-" * 80)
            for subject, stats in sorted(perf.items()):
                print(f"\n{subject}:")
                print(f"  Total Hours: {stats['total_hours']:.2f}")
                print(f"  Sessions: {stats['sessions']}")
                print(f"  Avg Productivity: {stats['avg_productivity']:.2f}/5")
                print(f"  Active Period: {stats['first_session']} to {stats['last_session']}")
        else:
            print("No subject data available yet.")
        
        # Overall statistics
        print("\n" + "-"*80)
        print("OVERALL STATISTICS:")
        print("-" * 80)
        
        if not self.tracker.df.empty:
            total_hours = self.tracker.df['hours_studied'].sum()
            total_sessions = len(self.tracker.df)
            avg_productivity = self.tracker.df['productivity_level'].mean()
            
            print(f"\nTotal Study Hours: {total_hours:.2f}")
            print(f"Total Sessions: {total_sessions}")
            print(f"Average Productivity: {avg_productivity:.2f}/5.0")
            print(f"Average Session Duration: {total_hours/total_sessions if total_sessions > 0 else 0:.2f} hours")
        else:
            print("\nNo data available. Start logging sessions to see statistics!")
        
        input("\nPress Enter to continue...")
    
    def show_help(self):
        """Show help and guide"""
        self.clear_screen()
        
        print("""
        ╔════════════════════════════════════════════════════════════════════════╗
        ║              AI STUDY TRACKER - COMPLETE USER GUIDE                    ║
        ╚════════════════════════════════════════════════════════════════════════╝
        
        📚 FEATURES:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        1. DAILY TRACKING
           • Log your study sessions day by day
           • Track subject name, hours studied, and productivity level
           • Add notes for each session
           • View today's summary anytime
        
        2. WEEKLY REPORTS
           • Comprehensive analysis of your weekly study patterns
           • Subject-wise performance breakdown
           • Consistency and productivity metrics
           • Exam readiness score (0-100)
           • Personalized recommendations
        
        3. STUDY TIMETABLES
           • AI-generated optimal weekly schedule
           • Based on your performance and study patterns
           • Prioritized by subject performance
           • Time slots based on your productivity hours
        
        4. SUBJECT RECOMMENDATIONS
           • Priority ranking of subjects to focus on
           • Study tips specific to each subject
           • Recommended hours per week
           • Performance-based suggestions
        
        5. PROGRESS ANALYTICS
           • Track your improvement over time
           • Subject-wise progress visualization
           • Study habits analysis
           • Consistency tracking
        
        
        📋 HOW TO USE:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        STEP 1: Log Daily Sessions
        └─ Go to "Daily Tracking" → "Add new study session"
        └─ Enter subject name, hours studied, and productivity level
        └─ Complete at least a few days of logging
        
        STEP 2: Check Weekly Report
        └─ Go to "Weekly Report" after logging data for a week
        └─ Review your performance metrics and readiness score
        └─ Check recommendations for improvement
        
        STEP 3: Generate Study Timetable
        └─ Go to "Generate Study Timetable"
        └─ System creates personalized optimal schedule
        └─ Follow the recommended time slots and subjects
        
        STEP 4: Follow Subject Recommendations
        └─ Review prioritized list of subjects to focus on
        └─ Adjust study time based on performance ratings
        └─ Use tips to improve productivity
        
        STEP 5: Monitor Progress
        └─ Regularly check "View Progress" section
        └─ Adjust study plan if needed
        └─ Keep logging sessions consistently
        
        
        💡 TIPS FOR BEST RESULTS:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        ✓ Log sessions DAILY for accurate analysis
        ✓ Be honest about productivity levels (don't overrate)
        ✓ Follow the AI-generated timetable for optimal results
        ✓ Review weekly reports every Sunday for planning next week
        ✓ Adjust study time if exam readiness score is below 50
        ✓ Sleep 7-8 hours daily for better retention
        ✓ Take 10-15 min breaks every 45-50 minutes of study
        ✓ Study in distraction-free environment
        
        
        🎯 PRODUCTIVITY LEVELS GUIDE:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        1 (Poor):           Very distracted, couldn't focus well
        2 (Below Average):  Some focus issues, got distracted frequently
        3 (Average):        Normal focus, some distractions
        4 (Good):           Good focus, minimal distractions
        5 (Excellent):      Perfect focus, very productive session
        
        
        📊 EXAM READINESS SCORE INTERPRETATION:
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        
        80-100:  EXCELLENT - Well prepared, ready for exam
        65-79:   GOOD - On track, minor improvements possible
        50-64:   MODERATE - Needs more study time and focus
        < 50:    NEEDS IMPROVEMENT - Significant effort required
        
        """)
        
        input("\nPress Enter to return to main menu...")
    
    def run(self):
        """Main application loop"""
        while self.running:
            self.display_main_menu()
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.run_daily_tracker()
            
            elif choice == '2':
                self.run_weekly_report()
            
            elif choice == '3':
                self.run_timetable_generator()
            
            elif choice == '4':
                self.show_recommendations()
            
            elif choice == '5':
                self.show_progress()
            
            elif choice == '6':
                self.show_help()
            
            elif choice == '7':
                print("\n" + "="*80)
                print("Thank you for using AI Study Tracker!")
                print("Keep studying and achieving your goals! 🎓")
                print("="*80 + "\n")
                self.running = False
            
            else:
                print("\n❌ Invalid choice. Please enter 1-7.")
                input("Press Enter to continue...")

def main():
    """Entry point"""
    app = StudyTrackerApp()
    app.run()

if __name__ == "__main__":
    main()
