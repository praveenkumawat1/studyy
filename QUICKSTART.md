QUICK START GUIDE
=================

AI-Based Study Tracker & Exam Readiness Analyzer
Version 1.0.0

## ⚡ 5-MINUTE SETUP

### 1. Install Dependencies (ONE TIME)
```bash
pip install pandas scikit-learn numpy joblib
```

### 2. Train ML Model (ONE TIME)
```bash
python train_model_enhanced.py
```

This will:
✓ Process student_data.csv
✓ Perform 5-fold cross-validation
✓ Detect overfitting/underfitting
✓ Save best model: best_student_model.pkl

Expected output:
- Training time: ~30 seconds
- Best model: Ridge Regression (R² = 0.7672)
- Files created: best_student_model.pkl

### 3. Start Application
```bash
python study_tracker_app.py
```

## 📖 TYPICAL DAILY WORKFLOW

### Every Day (Evening)
```
1. Run: python study_tracker_app.py
2. Select: 1 (Daily Tracking)
3. Select: 1 (Add new study session)
4. Log your sessions:
   - Subject: Mathematics
   - Hours: 2.5
   - Productivity: 4 (out of 5)
   - Notes: (optional)
5. Repeat for each study session
6. Exit when done
```

Time required: 2-3 minutes per day

### Every Sunday (Weekly Analysis)
```
1. Run: python study_tracker_app.py
2. Select: 2 (Weekly Report)
   - Review exam readiness score
   - Check recommendations
3. Select: 3 (Generate Study Timetable)
   - Get AI-optimized schedule
   - Review subject priorities
4. Select: 4 (Subject Recommendations)
   - See which subjects need focus
5. Plan next week accordingly
```

Time required: 10-15 minutes

## 🎯 STEP-BY-STEP EXAMPLE

### Day 1 - Monday Study Session

```
$ python study_tracker_app.py

Menu appears...
Enter: 1
Enter: 1 (Add new study session)

--- Study Session 1 ---
Subject: Mathematics
Hours: 2.5
Productivity Level (1-5): 4
Notes: Completed Chapter 5 exercises

--- Study Session 2 ---
Subject: Physics
Hours: 1.5
Productivity Level (1-5): 3
Notes: Reviewed kinematics concepts

--- Study Session 3 ---
Subject: Chemistry
Hours: 2
Productivity Level (1-5): 4
Notes: Practiced balancing equations

Done
Enter 'done' to finish

✓ 3 sessions saved!
```

### End of Week - Sunday Analysis

```
$ python study_tracker_app.py
Enter: 2 (Weekly Report)

Output:
───────────────────────────────────────
WEEKLY SUMMARY
───────────────────────────────────────
Total Study Hours: 42.5 hours
Average Daily: 6.1 hours
Total Sessions: 24
Subjects Covered: 4

EXAM READINESS: 78/100 (GOOD)

RECOMMENDATIONS:
✓ Great study volume
• Increase Physics focus
• Chemistry productivity needs work
• Study at least 5-6 days/week

───────────────────────────────────────

Save report? (y/n): y
✓ Report saved as 'weekly_report_2026-03-13.txt'
```

```
Enter: 3 (Generate Study Timetable)

OPTIMIZED WEEKLY STUDY TIMETABLE
─────────────────────────────────────

MONDAY
06:00-07:00 | Mathematics    | 1.0h | Average
10:00-11:00 | Physics        | 1.0h | Needs Improvement
17:00-18:00 | Chemistry      | 1.0h | Average

TUESDAY
06:00-07:00 | Chemistry      | 1.0h | Average
...

[More days...]

Save timetable? (y/n): y
✓ Timetable saved as 'study_timetable_2026-03-13.txt'
```

## 📊 KEY METRICS EXPLAINED

### Productivity Levels
- **1 (Poor)**: Very distracted, couldn't focus
- **2 (Below Avg)**: Some focus issues
- **3 (Average)**: Normal focus, some distractions
- **4 (Good)**: Good focus, minimal distractions
- **5 (Excellent)**: Perfect focus, very productive

### Exam Readiness Score
- **80-100**: EXCELLENT - Ready for exam
- **65-79**: GOOD - On track
- **50-64**: MODERATE - Needs improvement
- **0-49**: POOR - Significant effort needed

### Study Consistency
- **0.8-1.0**: Excellent - Very consistent
- **0.6-0.8**: Good - Mostly consistent
- **0.4-0.6**: Average - Some inconsistency
- **0.0-0.4**: Poor - Very inconsistent

## 📁 FILES EXPLAINED

### Generated During Use
- `daily_study_log.csv` - All your study sessions
- `weekly_report_[date].txt` - Weekly analysis
- `study_timetable_[date].txt` - Your study schedule

### Core System Files
- `preprocess_data.py` - Data preparation
- `train_model_enhanced.py` - ML model training
- `daily_tracker.py` - Daily logging
- `weekly_report.py` - Weekly analysis
- `timetable_generator.py` - Schedule creation
- `study_tracker_app.py` - Main application

### Required Data
- `student_data.csv` - Training data (included)
- `best_student_model.pkl` - ML model (created on first training)

## ✅ TESTING THE SYSTEM

To verify everything works:

```bash
python test_system.py
```

This will:
✓ Generate sample data
✓ Test all modules
✓ Verify ML model
✓ Display test results

Expected output:
```
Results: 4/4 tests passed
🎉 ALL TESTS PASSED! System is ready to use.
```

## 🐛 TROUBLESHOOTING

### Issue: "No such file or directory: best_student_model.pkl"
**Solution**: Run training first
```bash
python train_model_enhanced.py
```

### Issue: "No sessions logged today"
**Solution**: Normal if using different day. Just log your current sessions.

### Issue: "No data available for this week"
**Solution**: Ensure you've logged sessions for at least 3-4 days.

### Issue: Module not found error
**Solution**: Ensure all .py files are in the same directory.

### Issue: CSV encoding error
**Solution**: The system uses UTF-8. Ensure your system supports it.

## 💡 TIPS FOR SUCCESS

1. **Log Immediately**: Record sessions right after studying
2. **Be Honest**: Rate productivity accurately (don't cheat!)
3. **Consistent Names**: Use same subject names (e.g., "Math" not "Maths")
4. **Follow Plan**: Stick to the AI-generated timetable
5. **Weekly Review**: Check reports every Sunday
6. **Adjust**: If readiness < 50, increase study time
7. **Sleep**: 7-8 hours daily improves memory
8. **Breaks**: 10-15 min breaks every 45-50 min

## 📈 EXPECTED RESULTS

### Week 1-2
- Get familiar with logging
- See initial patterns
- Readiness score: 40-60

### Week 3-4
- More accurate data
- Better recommendations
- Readiness score: 55-75

### Week 5-8
- Consistent improvements
- Optimized schedule
- Readiness score: 70-90

## 🎓 SYSTEM ARCHITECTURE

```
Your Daily Input
       ↓
[Daily Tracker] → daily_study_log.csv
       ↓
[Weekly Report] ← [Machine Learning Model]
       ↓
[Recommendations]
       ↓
[Timetable Generator]
       ↓
Your Optimized Schedule
```

## 🚀 ADVANCED FEATURES

### View Detailed Analytics
```bash
python weekly_report.py  # Standalone weekly analysis
python timetable_generator.py  # Standalone timetable
```

### Process Raw Data
```bash
python preprocess_data.py  # See preprocessing pipeline
```

### Retrain Model
```bash
python train_model_enhanced.py  # Update model with latest data
```

## 📞 SUPPORT

### Common Questions

**Q: How often should I log sessions?**
A: Every study session, ideally within a few minutes of completing it.

**Q: Can I edit previous sessions?**
A: Check the daily_study_log.csv file and edit directly (advanced).

**Q: How accurate is the exam readiness score?**
A: Based on your actual study patterns. More data = more accurate.

**Q: Should I follow the timetable exactly?**
A: Use it as a guide. Flexibility is important too.

**Q: How long until I see improvements?**
A: Results visible after 2 weeks, significant improvements after 4-6 weeks.

## 📋 CHECKLIST

Before First Use:
- [ ] Python 3.8+ installed
- [ ] Dependencies installed
- [ ] Model trained
- [ ] Test system passed

Daily (Evening):
- [ ] Log all study sessions
- [ ] Rate productivity honestly
- [ ] Check daily summary

Weekly (Sunday):
- [ ] Review weekly report
- [ ] Generate new timetable
- [ ] Check recommendations
- [ ] Plan next week

## 🎉 GET STARTED!

1. Ensure dependencies installed:
   ```bash
   pip install pandas scikit-learn numpy joblib
   ```

2. Train the model:
   ```bash
   python train_model_enhanced.py
   ```

3. Start tracking:
   ```bash
   python study_tracker_app.py
   ```

4. Follow the menu!

**Good luck with your studies! 📚🎓**

---

For detailed documentation, see: README.md
Last Updated: March 13, 2026
Version: 1.0.0
