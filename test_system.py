"""
System Test & Sample Data Generator
Tests all modules and creates sample data for demonstration
"""

import pandas as pd
from datetime import datetime, timedelta
import os
import sys

def generate_sample_data():
    """Generate sample study data for testing"""
    
    print("\n" + "="*80)
    print("GENERATING SAMPLE STUDY DATA")
    print("="*80 + "\n")
    
    # Create sample data for 2 weeks
    data = []
    start_date = datetime.now() - timedelta(days=14)
    
    subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'English']
    
    for day in range(14):
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime("%Y-%m-%d")
        
        # 2-4 sessions per day
        num_sessions = 2 + (day % 3)
        
        for session in range(num_sessions):
            subject = subjects[session % len(subjects)]
            hours = 1.5 + (session * 0.3)
            
            # Productivity increases towards end of week
            base_productivity = 2 + (day % 7 * 0.4)
            productivity = min(5, int(base_productivity + (session * 0.2)))
            
            data.append({
                'date': date_str,
                'time': f"{8 + session*2:02d}:00:00",
                'subject': subject,
                'hours_studied': round(hours, 2),
                'productivity_level': productivity,
                'notes': f'Session {session+1}' if session > 0 else ''
            })
    
    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv('daily_study_log_sample.csv', index=False)
    
    print(f"✓ Sample data created: {len(df)} sessions")
    print(f"  Date range: {data[0]['date']} to {data[-1]['date']}")
    print(f"  Subjects: {', '.join(subjects)}")
    print(f"\nData saved as 'daily_study_log_sample.csv'")
    
    return df

def test_daily_tracker():
    """Test daily tracker module"""
    print("\n" + "="*80)
    print("TESTING DAILY TRACKER MODULE")
    print("="*80 + "\n")
    
    try:
        from daily_tracker import DailyStudyTracker
        
        # Load sample data
        tracker = DailyStudyTracker('daily_study_log_sample.csv')
        
        # Test today's summary
        print("Testing today's summary...")
        today_summary = tracker.get_today_summary()
        if today_summary:
            print(f"✓ Today's data available")
            print(f"  Total hours: {today_summary['total_hours']:.2f}")
        else:
            print("✓ No today's data (expected if running on different day)")
        
        # Test week summary
        print("\nTesting week summary...")
        week_summary = tracker.get_week_summary()
        if week_summary:
            print(f"✓ Week summary available")
            print(f"  Total hours: {week_summary['total_hours']:.2f}")
            print(f"  Total sessions: {week_summary['total_sessions']}")
        
        # Test subject performance
        print("\nTesting subject performance...")
        perf = tracker.get_subject_performance()
        if perf:
            print(f"✓ Subject performance tracked: {len(perf)} subjects")
            for subject, stats in list(perf.items())[:2]:
                print(f"  {subject}: {stats['total_hours']:.2f}h ({stats['sessions']} sessions)")
        
        print("\n✓ Daily Tracker Module: PASSED")
        return True
    
    except Exception as e:
        print(f"❌ Daily Tracker Module: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_weekly_report():
    """Test weekly report module"""
    print("\n" + "="*80)
    print("TESTING WEEKLY REPORT MODULE")
    print("="*80 + "\n")
    
    try:
        from daily_tracker import DailyStudyTracker
        from weekly_report import WeeklyReportGenerator
        
        tracker = DailyStudyTracker('daily_study_log_sample.csv')
        report = WeeklyReportGenerator(tracker)
        
        print("Generating weekly report...")
        report_data = report.generate_report()
        
        if report_data:
            print("\n✓ Weekly Report Module: PASSED")
            return True
        else:
            print("\n⚠️ No report data generated")
            return False
    
    except Exception as e:
        print(f"❌ Weekly Report Module: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_timetable_generator():
    """Test timetable generator module"""
    print("\n" + "="*80)
    print("TESTING TIMETABLE GENERATOR MODULE")
    print("="*80 + "\n")
    
    try:
        from daily_tracker import DailyStudyTracker
        from weekly_report import WeeklyReportGenerator
        from timetable_generator import TimetableGenerator
        
        tracker = DailyStudyTracker('daily_study_log_sample.csv')
        report = WeeklyReportGenerator(tracker)
        
        # Ensure report is generated
        if not report.report:
            report.generate_report()
        
        timetable = TimetableGenerator(report)
        
        print("Generating timetable...")
        timetable_data = timetable.generate_weekly_timetable()
        
        if timetable_data:
            print("✓ Timetable generated successfully")
            
            # Count sessions
            total_sessions = sum(len(sessions) for sessions in timetable_data.values())
            print(f"  Total sessions scheduled: {total_sessions}")
            
            # Show sample
            for day, sessions in list(timetable_data.items())[:2]:
                if sessions:
                    print(f"  {day}: {len(sessions)} session(s)")
            
            print("\n✓ Timetable Generator Module: PASSED")
            return True
    
    except Exception as e:
        print(f"❌ Timetable Generator Module: FAILED - {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_model():
    """Test if trained model exists and works"""
    print("\n" + "="*80)
    print("TESTING ML MODEL")
    print("="*80 + "\n")
    
    try:
        import joblib
        
        if os.path.exists('best_student_model.pkl'):
            print("✓ Model file found")
            
            model = joblib.load('best_student_model.pkl')
            print(f"✓ Model loaded successfully")
            print(f"  Model type: {type(model).__name__}")
            
            print("\n✓ ML Model: PASSED")
            return True
        else:
            print("❌ Model file not found: best_student_model.pkl")
            print("   Run: python train_model_enhanced.py")
            return False
    
    except Exception as e:
        print(f"❌ ML Model: FAILED - {str(e)}")
        return False

def run_all_tests():
    """Run all tests"""
    print("\n\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*20 + "AI STUDY TRACKER - SYSTEM TEST" + " "*30 + "║")
    print("╚" + "="*78 + "╝")
    
    # Generate sample data first
    generate_sample_data()
    
    # Run tests
    results = {
        'Daily Tracker': test_daily_tracker(),
        'Weekly Report': test_weekly_report(),
        'Timetable Generator': test_timetable_generator(),
        'ML Model': test_model()
    }
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80 + "\n")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for module, result in results.items():
        status = "✓ PASSED" if result else "❌ FAILED"
        print(f"{module:25} {status}")
    
    print("\n" + "-"*80)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nTo start using the system, run:")
        print("  python study_tracker_app.py")
    else:
        print("\n❌ Some tests failed. Review the errors above.")
    
    print("\n" + "="*80 + "\n")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
