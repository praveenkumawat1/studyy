"""
Daily Timetable Generator for Next Day
Based on user sessions - recommends subjects/time slots
"""
import json
from datetime import datetime, timedelta
from db_config import DatabaseConfig
from db_operations import StudySessionDB, SubjectPerformanceDB

class NextDayTimetableGenerator:
    def __init__(self, user_id):
        self.user_id = user_id
        self.timetable = []
        self.recommendations = []
    
    def get_user_subjects(self):
        """Get user's recent subjects and performance"""
        subject_db = SubjectPerformanceDB()
        performance = subject_db.get_subject_performance(self.user_id)
        
        if not performance:
            return []
        
        # Sort by performance (lowest first - needs most attention)
        sorted_subjects = sorted(performance.items(), key=lambda x: x[1]['avg_productivity'])
        
        return sorted_subjects[:3]  # Top 3 subjects
    
    def get_available_slots(self):
        """Default productive time slots"""
        return [
            "6:00-7:00 AM - Morning Focus",
            "7:00-8:00 AM - Memory Peak", 
            "8:00-9:00 AM - High Concentration",
            "5:00-6:00 PM - Evening Review",
            "6:00-7:00 PM - Problem Solving",
            "7:00-8:00 PM - Light Revision"
        ]
    
    def generate_next_day_timetable(self):
        """Generate recommended timetable for next day"""
        subjects = self.get_user_subjects()
        
        if not subjects:
            self.timetable = []
            self.recommendations = ["Log some study sessions first to get personalized recommendations!"]
            return self.timetable
        
        slots = self.get_available_slots()
        total_slots = len(slots)
        
        timetable = []
        for i, (subject, perf) in enumerate(subjects):
            if i < total_slots:
                slot = slots[i]
                timetable.append({
                    "time": slot,
                    "subject": subject,
                    "duration": "1 hour",
                    "reason": f"Low performance ({perf['avg_productivity']:.1f}/5) - Priority"
                })
        
        # Fill remaining slots with review
        if len(timetable) < total_slots:
            for i in range(len(timetable), total_slots):
                timetable.append({
                    "time": slots[i],
                    "subject": "Review & Revision",
                    "duration": "45 minutes", 
                    "reason": "Consolidate today's learning"
                })
        
        self.timetable = timetable
        self.generate_recommendations(subjects)
        
        return self.timetable
    
    def generate_recommendations(self, subjects):
        """Generate personalized recommendations"""
        recs = []
        
        for subject, perf in subjects:
            hours = perf['hours']
            prod = perf['avg_productivity']
            
            if prod < 3:
                recs.append(f"Study {subject} more - low productivity ({prod:.1f})")
            if hours < 5:
                recs.append(f"Revise {subject} - only {hours:.1f}h logged this week")
        
        recs.append("Take 5-10 min breaks between sessions")
        recs.append("Stay hydrated and avoid distractions")
        
        self.recommendations = recs[:3]  # Top 3

