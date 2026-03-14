"""
Daily Study Tracking System
Allows students to log:
- Study sessions per day
- Subject names
- Hours studied
- Productivity level
"""

import pandas as pd
from datetime import datetime
import json
import os

class DailyStudyTracker:
    def __init__(self, data_file='daily_study_log.csv'):
        self.data_file = data_file
        self.session_data = []
        self.load_existing_data()
    
    def load_existing_data(self):
        """Load existing study logs"""
        if os.path.exists(self.data_file):
            self.df = pd.read_csv(self.data_file)
        else:
            self.df = pd.DataFrame()
    
    def add_study_session(self, subject, hours, productivity_level=3, notes=""):
        """
        Add a single study session
        
        Args:
            subject: Subject name
            hours: Hours studied
            productivity_level: 1-5 scale (1=low, 5=high)
            notes: Additional notes
        """
        session = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'time': datetime.now().strftime("%H:%M:%S"),
            'subject': subject.strip().title(),
            'hours_studied': float(hours),
            'productivity_level': int(productivity_level),
            'notes': notes
        }
        
        self.session_data.append(session)
        return session
    
    def log_daily_sessions(self):
        """Interactive daily session logging"""
        print("\n" + "="*60)
        print("DAILY STUDY TRACKER - LOG YOUR SESSIONS")
        print("="*60 + "\n")
        
        today = datetime.now().strftime("%Y-%m-%d")
        print(f"Today's Date: {today}\n")
        
        session_count = 0
        
        while True:
            print(f"\n--- Study Session {session_count + 1} ---\n")
            
            subject = input("Enter subject name (or 'done' to finish): ").strip()
            if subject.lower() == 'done':
                break
            
            if not subject:
                print("❌ Subject name cannot be empty!")
                continue
            
            try:
                hours = float(input("Hours studied: "))
                if hours <= 0:
                    print("❌ Hours must be greater than 0!")
                    continue
            except ValueError:
                print("❌ Invalid input. Please enter a number!")
                continue
            
            print("\nProductivity Level (1=Poor, 5=Excellent):")
            try:
                productivity = int(input("Enter level (1-5): "))
                if productivity < 1 or productivity > 5:
                    print("❌ Please enter a number between 1-5!")
                    continue
            except ValueError:
                print("❌ Invalid input. Please enter a number!")
                continue
            
            notes = input("Add notes (optional): ").strip()
            
            session = self.add_study_session(subject, hours, productivity, notes)
            print(f"\n✓ Logged: {subject} - {hours} hours (Productivity: {productivity}/5)")
            session_count += 1
        
        if session_count > 0:
            self.save_sessions()
            print(f"\n✓ {session_count} session(s) saved!")
        else:
            print("No sessions logged today.")
    
    def save_sessions(self):
        """Save sessions to CSV"""
        if self.session_data:
            new_df = pd.DataFrame(self.session_data)
            
            if not self.df.empty:
                self.df = pd.concat([self.df, new_df], ignore_index=True)
            else:
                self.df = new_df
            
            self.df.to_csv(self.data_file, index=False)
            print(f"✓ Sessions saved to {self.data_file}")
            self.session_data = []  # Reset
    
    def get_today_summary(self):
        """Get today's study summary"""
        if self.df.empty:
            return None
        
        today = datetime.now().strftime("%Y-%m-%d")
        today_data = self.df[self.df['date'] == today]
        
        if today_data.empty:
            return None
        
        summary = {
            'date': today,
            'total_hours': today_data['hours_studied'].sum(),
            'sessions': len(today_data),
            'subjects': today_data['subject'].unique().tolist(),
            'avg_productivity': today_data['productivity_level'].mean(),
            'sessions_detail': today_data.to_dict('records')
        }
        
        return summary
    
    def get_week_summary(self):
        """Get this week's study summary"""
        if self.df.empty:
            return None
        
        self.df['date'] = pd.to_datetime(self.df['date'])
        today = pd.Timestamp.now()
        week_start = today - pd.Timedelta(days=today.weekday())
        week_end = week_start + pd.Timedelta(days=6)
        
        week_data = self.df[(self.df['date'] >= week_start) & (self.df['date'] <= week_end)]
        
        if week_data.empty:
            return None
        
        summary = {
            'week_start': week_start.strftime("%Y-%m-%d"),
            'week_end': week_end.strftime("%Y-%m-%d"),
            'total_hours': week_data['hours_studied'].sum(),
            'total_sessions': len(week_data),
            'subjects': week_data['subject'].unique().tolist(),
            'avg_productivity': week_data['productivity_level'].mean(),
            'daily_breakdown': {}
        }
        
        for date in week_data['date'].unique():
            day_data = week_data[week_data['date'] == date]
            summary['daily_breakdown'][date.strftime("%Y-%m-%d")] = {
                'hours': day_data['hours_studied'].sum(),
                'sessions': len(day_data),
                'avg_productivity': day_data['productivity_level'].mean()
            }
        
        return summary
    
    def get_subject_performance(self):
        """Get performance by subject"""
        if self.df.empty:
            return None
        
        performance = {}
        for subject in self.df['subject'].unique():
            subject_data = self.df[self.df['subject'] == subject]
            performance[subject] = {
                'total_hours': subject_data['hours_studied'].sum(),
                'sessions': len(subject_data),
                'avg_productivity': subject_data['productivity_level'].mean(),
                'first_session': subject_data['date'].min(),
                'last_session': subject_data['date'].max()
            }
        
        return performance

def main():
    tracker = DailyStudyTracker()
    
    while True:
        print("\n" + "="*60)
        print("DAILY STUDY TRACKER")
        print("="*60)
        print("\n1. Log Study Session")
        print("2. View Today's Summary")
        print("3. View Week's Summary")
        print("4. View Subject Performance")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            tracker.log_daily_sessions()
        
        elif choice == '2':
            summary = tracker.get_today_summary()
            if summary:
                print("\n" + "="*60)
                print("TODAY'S STUDY SUMMARY")
                print("="*60)
                print(f"Date: {summary['date']}")
                print(f"Total Hours: {summary['total_hours']:.2f}")
                print(f"Sessions: {summary['sessions']}")
                print(f"Subjects: {', '.join(summary['subjects'])}")
                print(f"Average Productivity: {summary['avg_productivity']:.2f}/5")
                
                print("\nSession Details:")
                for i, sess in enumerate(summary['sessions_detail'], 1):
                    print(f"  {i}. {sess['subject']} - {sess['hours_studied']}h (Productivity: {sess['productivity_level']}/5)")
            else:
                print("No sessions logged today.")
        
        elif choice == '3':
            summary = tracker.get_week_summary()
            if summary:
                print("\n" + "="*60)
                print("WEEKLY STUDY SUMMARY")
                print("="*60)
                print(f"Week: {summary['week_start']} to {summary['week_end']}")
                print(f"Total Hours: {summary['total_hours']:.2f}")
                print(f"Total Sessions: {summary['total_sessions']}")
                print(f"Subjects: {', '.join(summary['subjects'])}")
                print(f"Average Productivity: {summary['avg_productivity']:.2f}/5")
            else:
                print("No sessions logged this week.")
        
        elif choice == '4':
            perf = tracker.get_subject_performance()
            if perf:
                print("\n" + "="*60)
                print("SUBJECT PERFORMANCE")
                print("="*60)
                for subject, stats in sorted(perf.items()):
                    print(f"\n{subject}:")
                    print(f"  Total Hours: {stats['total_hours']:.2f}")
                    print(f"  Sessions: {stats['sessions']}")
                    print(f"  Avg Productivity: {stats['avg_productivity']:.2f}/5")
            else:
                print("No data available.")
        
        elif choice == '5':
            print("\nThank you for using Daily Study Tracker!")
            break
        
        else:
            print("❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
