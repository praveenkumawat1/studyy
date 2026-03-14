## TODO - Smart Study Tracker Enhancements

### Current Status
- ✅ Backend API running
- ✅ Frontend running 
- ✅ User registration/login working
- ✅ Sessions add/delete working
- ✅ Weekly reports (global data)

### Required Fixes (High Priority)
1. **Fix /api/sessions/today 500 error** - DB row format dict/list mismatch
2. **Fix /api/reports/weekly 500** - WeeklyReportGenerator __init__ expects tracker, not user_id
3. **Make reports user-specific** - Pass user_id to get user DB data

### New Features (Overview Page Only)
1. **Productivity Detection Rule:**
   ```
   > 40min → Productive (4-5)
   < 20min → Unproductive (1-2)
   ```
   Display status badge with sessions

2. **Exam Readiness Report (Daily/Weekly):**
   ```
   Exam Readiness : 78%
   Status : Almost Ready
   Recommendation : Study DBMS more
   ```
   - Use existing Random Forest model
   - Daily & Weekly sections
   - Clean UI integration

### Implementation Plan
```
1. Fix db_operations.py get_*_sessions → consistent tuple/list format
2. Update WeeklyReportGenerator __init__(user_id) → use StudySessionDB
3. Frontend Dashboard.js → Add productivity logic + readiness UI
4. Test new user flow
```

**Next Step:** Fix API 500 errors first
