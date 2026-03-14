"""
Weekly Report Generator
Analyzes:
- Weekly study patterns
- Subject performance
- Productivity trends
- Exam readiness predictions
- Study recommendations
"""

import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from daily_tracker import DailyStudyTracker
import joblib

class WeeklyReportGenerator:
    def __init__(self, tracker=None, model_path='best_student_model.pkl'):
        self.tracker = tracker or DailyStudyTracker()
        try:
            self.productivity_scaler = joblib.load('productivity_scaler.pkl')
            self.productivity_model = joblib.load('productivity_model.pkl')
            self.exam_scaler = joblib.load('exam_readiness_scaler.pkl')
            self.exam_model = joblib.load('exam_readiness_model.pkl')
            self.has_models = True
        except:
            self.productivity_scaler = None
            self.productivity_model = None
            self.exam_scaler = None
            self.exam_model = None
            self.has_models = False
        
        self.report = {}
    
    def calculate_metrics(self):
        """Calculate weekly metrics"""
        week_summary = self.tracker.get_week_summary()
        
        if not week_summary:
            print("No data available for this week.")
            return None
        
        subject_performance = self.tracker.get_subject_performance()
        
        metrics = {
            'week_start': week_summary['week_start'],
            'week_end': week_summary['week_end'],
            'total_study_hours': week_summary['total_hours'],
            'total_sessions': week_summary['total_sessions'],
            'daily_average': week_summary['total_hours'] / 7,
            'avg_productivity': week_summary['avg_productivity'],
            'subjects_covered': len(week_summary['subjects']),
            'daily_breakdown': week_summary['daily_breakdown'],
            'subject_details': subject_performance
        }
        
        self.report['metrics'] = metrics
        return metrics
    
    def analyze_study_patterns(self):
        """Analyze study patterns and habits"""
        metrics = self.report.get('metrics')
        if not metrics:
            return None
        
        daily_hours = list(metrics['daily_breakdown'].values())
        hours = [d.get('hours', 0) for d in daily_hours]
        
        pattern_analysis = {
            'most_active_day': max(metrics['daily_breakdown'].items(), 
                                  key=lambda x: x[1]['hours'])[0],
            'least_active_day': min(metrics['daily_breakdown'].items(), 
                                   key=lambda x: x[1]['hours'])[0],
            'consistency': self._calculate_consistency(hours),
            'peak_productivity_rating': max([d.get('avg_productivity', 0) 
                                            for d in daily_hours]),
            'study_frequency': {
                'days_studied': sum([1 for h in hours if h > 0]),
                'total_days': 7,
                'study_rate': f"{(sum([1 for h in hours if h > 0]) / 7) * 100:.1f}%"
            }
        }
        
        self.report['patterns'] = pattern_analysis
        return pattern_analysis
    
    def _calculate_consistency(self, hours_list):
        """Calculate study consistency (0-1 scale)"""
        if not hours_list or all(h == 0 for h in hours_list):
            return 0
        
        study_hours = [h for h in hours_list if h > 0]
        if len(study_hours) == 0:
            return 0
        
        variance = np.var(study_hours)
        consistency = 1 / (1 + variance)
        return min(consistency, 1.0)
    
    def subject_analysis(self):
        """Analyze performance per subject"""
        subject_perf = self.report['metrics'].get('subject_details', {})
        
        if not subject_perf:
            return None
        
        subject_analysis = {}
        for subject, stats in subject_perf.items():
            # Productivity rating
            if stats['avg_productivity'] >= 4.5:
                rating = "Excellent"
            elif stats['avg_productivity'] >= 3.5:
                rating = "Good"
            elif stats['avg_productivity'] >= 2.5:
                rating = "Average"
            else:
                rating = "Needs Improvement"
            
            subject_analysis[subject] = {
                'hours': stats['total_hours'],
                'sessions': stats['sessions'],
                'avg_productivity_score': round(stats['avg_productivity'], 2),
                'productivity_rating': rating,
                'focus_intensity': stats['total_hours'] / stats['sessions'] if stats['sessions'] > 0 else 0
            }
        
        self.report['subject_analysis'] = subject_analysis
        return subject_analysis
    
    def generate_recommendations(self):
        """Generate personalized study recommendations"""
        metrics = self.report.get('metrics')
        patterns = self.report.get('patterns')
        subject_analysis = self.report.get('subject_analysis')
        
        recommendations = []
        
        # Based on total hours
        if metrics['total_study_hours'] < 10:
            recommendations.append("⚠️  LOW STUDY VOLUME: Aim for at least 10-15 hours per week")
        elif metrics['total_study_hours'] > 30:
            recommendations.append("✓ HIGH ENGAGEMENT: Great study commitment! Watch out for fatigue")
        
        # Based on consistency
        consistency = patterns.get('consistency', 0)
        if consistency < 0.6:
            recommendations.append("📊 IRREGULAR SCHEDULE: Try to maintain consistent study hours across days")
        
        # Based on productivity
        if metrics['avg_productivity'] < 3:
            recommendations.append("🎯 LOW PRODUCTIVITY: Review your study environment and techniques")
        
        # Study frequency
        study_rate = patterns['study_frequency']['days_studied']
        if study_rate < 4:
            recommendations.append("📅 INCREASE FREQUENCY: Study at least 5-6 days per week")
        
        # Subject-specific
        for subject, analysis in subject_analysis.items():
            if analysis['productivity_rating'] == 'Needs Improvement':
                recommendations.append(f"🔄 {subject}: Consider different study methods or timing")
            
            if analysis['hours'] < 2:
                recommendations.append(f"📚 {subject}: Increase focus on this subject (currently {analysis['hours']:.1f}h)")
        
        # Positive feedback
        if metrics['total_study_hours'] >= 15 and metrics['avg_productivity'] >= 3.5:
            recommendations.append("🌟 EXCELLENT PROGRESS: You're on track for great exam performance!")
        
        self.report['recommendations'] = recommendations
        return recommendations
    
    def predict_exam_readiness(self):
        """ML Predict exam readiness score"""
        metrics = self.report.get('metrics')
        patterns = self.report.get('patterns', {})
        
        if not self.has_models or not metrics:
            # Fallback to rule-based
            # ... (keep original code)
            readiness_components = {
                'study_hours_score': min((metrics['total_study_hours'] / 20) * 30, 30),
                'consistency_score': patterns.get('consistency', 0) * 20,
                'productivity_score': min((metrics['avg_productivity'] / 5) * 30, 30),
                'coverage_score': min((metrics['subjects_covered'] / 5) * 20, 20)
            }
            total_readiness = sum(readiness_components.values())
            status = self._get_status(total_readiness)
            self.report['exam_readiness'] = {'score': round(total_readiness, 1), 'status': status}
            return self.report['exam_readiness']
        
        # ML prediction
        features = np.array([[metrics['total_study_hours'], 
                             metrics['subjects_covered'], 
                             patterns.get('study_days', 1), 
                             metrics['avg_productivity'], 
                             patterns.get('consistency', 0)]])
        
        features_scaled = self.exam_scaler.transform(features)
        readiness = self.exam_model.predict(features_scaled)[0]
        
        status = self._get_status(readiness)
        
        self.report['exam_readiness'] = {
            'score': round(readiness, 1),
            'status': status,
            'method': 'ML Prediction'
        }
        return self.report['exam_readiness']
    
    def _get_status(self, score):
        if score >= 80:
            return "EXCELLENT"
        elif score >= 65:
            return "GOOD"
        elif score >= 50:
            return "MODERATE"
        else:
            return "NEEDS IMPROVEMENT"
    
    def generate_report(self):
        """Generate complete weekly report"""
        print("\n" + "="*70)
        print("WEEKLY STUDY REPORT")
        print("="*70)
        
        # Calculate metrics
        self.calculate_metrics()
        if not self.report.get('metrics'):
            return None
        
        metrics = self.report['metrics']
        
        # Analysis
        self.analyze_study_patterns()
        self.subject_analysis()
        self.generate_recommendations()
        self.predict_exam_readiness()
        
        # Display report
        print(f"\nWeek: {metrics['week_start']} to {metrics['week_end']}")
        print(f"\n{'─'*70}")
        print("STUDY SUMMARY")
        print(f"{'─'*70}")
        print(f"Total Study Hours: {metrics['total_study_hours']:.2f} hours")
        print(f"Average Daily Study: {metrics['daily_average']:.2f} hours")
        print(f"Total Sessions: {metrics['total_sessions']}")
        print(f"Subjects Covered: {metrics['subjects_covered']}")
        print(f"Average Productivity: {metrics['avg_productivity']:.2f}/5.0")
        
        patterns = self.report.get('patterns', {})
        print(f"\n{'─'*70}")
        print("STUDY PATTERNS")
        print(f"{'─'*70}")
        print(f"Most Active: {patterns.get('most_active_day', 'N/A')}")
        print(f"Least Active: {patterns.get('least_active_day', 'N/A')}")
        print(f"Study Consistency: {patterns.get('consistency', 0):.2f}/1.0")
        print(f"Days Studied: {patterns['study_frequency']['days_studied']}/7 ({patterns['study_frequency']['study_rate']})")
        
        subject_analysis = self.report.get('subject_analysis', {})
        print(f"\n{'─'*70}")
        print("SUBJECT PERFORMANCE")
        print(f"{'─'*70}")
        for subject, analysis in subject_analysis.items():
            print(f"\n{subject}:")
            print(f"  Hours: {analysis['hours']:.2f} | Sessions: {analysis['sessions']}")
            print(f"  Productivity: {analysis['avg_productivity_score']}/5.0 ({analysis['productivity_rating']})")
            print(f"  Focus Intensity: {analysis['focus_intensity']:.2f} h/session")
        
        exam_readiness = self.report.get('exam_readiness', {})
        print(f"\n{'─'*70}")
        print("EXAM READINESS ASSESSMENT")
        print(f"{'─'*70}")
        print(f"Readiness Score: {exam_readiness.get('score', 0)}/100")
        print(f"Status: {exam_readiness.get('status', 'Unknown')}")
        
        recommendations = self.report.get('recommendations', [])
        print(f"\n{'─'*70}")
        print("PERSONALIZED RECOMMENDATIONS")
        print(f"{'─'*70}")
        if recommendations:
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec}")
        else:
            print("Keep maintaining your current study routine!")
        
        print(f"\n{'='*70}\n")
        
        return self.report
    
    def save_report(self, filename=None):
        """Save report to file"""
        if not filename:
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"weekly_report_{today}.txt"
        
        with open(filename, 'w') as f:
            f.write("WEEKLY STUDY REPORT\n")
            f.write("="*70 + "\n\n")
            
            metrics = self.report.get('metrics', {})
            f.write(f"Week: {metrics.get('week_start')} to {metrics.get('week_end')}\n\n")
            
            f.write("STUDY SUMMARY\n")
            f.write("-"*70 + "\n")
            f.write(f"Total Study Hours: {metrics.get('total_study_hours', 0):.2f}\n")
            f.write(f"Average Daily: {metrics.get('daily_average', 0):.2f}\n")
            f.write(f"Subjects Covered: {metrics.get('subjects_covered', 0)}\n")
            f.write(f"Average Productivity: {metrics.get('avg_productivity', 0):.2f}/5.0\n\n")
            
            exam_readiness = self.report.get('exam_readiness', {})
            f.write("EXAM READINESS\n")
            f.write("-"*70 + "\n")
            f.write(f"Score: {exam_readiness.get('score', 0)}/100\n")
            f.write(f"Status: {exam_readiness.get('status', 'Unknown')}\n\n")
            
            recommendations = self.report.get('recommendations', [])
            f.write("RECOMMENDATIONS\n")
            f.write("-"*70 + "\n")
            for rec in recommendations:
                f.write(f"• {rec}\n")
        
        print(f"✓ Report saved to {filename}")
        return filename

def main():
    tracker = DailyStudyTracker()
    report = WeeklyReportGenerator(tracker)
    report.generate_report()
    report.save_report()

if __name__ == "__main__":
    main()
