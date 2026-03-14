import React, { useState, useEffect } from 'react';
import Navigation from '../components/Navigation';
import { sessionsAPI, reportsAPI } from '../services/api';
import {
  PieChart, Pie, Cell, Tooltip, Legend
} from 'recharts';
import '../styles/Dashboard.css';

const Dashboard = () => {
  const [activePage, setActivePage] = useState('overview');
  const [todaySessions, setTodaySessions] = useState([]);
  const [weekSessions, setWeekSessions] = useState([]);
  const [weeklyReport, setWeeklyReport] = useState(null);
  const [newSession, setNewSession] = useState({
    subject: '',
    hours_studied: '',
    productivity_level: 3,
    notes: '',
    session_date: new Date().toISOString().split('T')[0],
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [nextDayTimetable, setNextDayTimetable] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

const fetchData = async () => {
    try {
      setLoading(true);
      const [todayRes, weekRes, reportRes] = await Promise.all([
        sessionsAPI.getTodaySessions().catch(() => ({ data: { sessions: [] } })),
        sessionsAPI.getWeekSessions().catch(() => ({ data: { sessions: [] } })),
        reportsAPI.getWeeklyReport().catch(() => ({ data: { report: null } })),
      ]);

      setTodaySessions(todayRes.data.sessions || []);
      setWeekSessions(weekRes.data.sessions || []);
      setWeeklyReport(reportRes.data.report || null);
    } catch (err) {
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchNextDayTimetable = async () => {
    try {
      const response = await sessionsAPI.getNextDayTimetable();  // Assume api.js has this
      setNextDayTimetable(response.data);
    } catch (err) {
      console.error('Error fetching timetable:', err);
    }
  };

  const handleSessionChange = (e) => {
    const { name, value } = e.target;
    setNewSession((prev) => ({
      ...prev,
      [name]: name === 'productivity_level' || name === 'hours_studied' ? Number(value) : value,
    }));
  };

  const handleAddSession = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (!newSession.subject || !newSession.hours_studied) {
      setError('Please fill all required fields');
      return;
    }

    try {
      setLoading(true);
      const response = await sessionsAPI.addSession({
        subject: newSession.subject,
        hours_studied: newSession.hours_studied,
        productivity_level: newSession.productivity_level,
        notes: newSession.notes,
        session_date: newSession.session_date,
      });

      if (response.data.success) {
        setMessage('Session added successfully!');
        setNewSession({
          subject: '',
          hours_studied: '',
          productivity_level: 3,
          notes: '',
          session_date: new Date().toISOString().split('T')[0],
        });
        setTimeout(() => {
          fetchData();
          setMessage('');
        }, 1500);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to add session');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = () => {
    const totalHours = weekSessions.reduce((sum, session) => sum + session.hours_studied, 0);
    const avgProductivity = weekSessions.length > 0
      ? (weekSessions.reduce((sum, session) => sum + session.productivity_level, 0) / weekSessions.length).toFixed(1)
      : 3.0; // default if no sessions

    // Productivity rule for sessions
    const productiveSessions = todaySessions.filter(session => session.hours_studied * 60 > 40);
    const unproductiveSessions = todaySessions.filter(session => session.hours_studied * 60 < 20);
    
    return {
      totalHours: totalHours.toFixed(1),
      totalSessions: weekSessions.length,
      avgProductivity,
      productiveCount: productiveSessions.length,
      unproductiveCount: unproductiveSessions.length,
      todaySessions: todaySessions,
    };
  };

  const stats = calculateStats();
  const subjects = [...new Set(weekSessions.map(s => s.subject))];

  // Subject hours data for pie chart
  const subjectData = subjects.map(subject => {
    const subjectHours = weekSessions
      .filter(s => s.subject === subject)
      .reduce((sum, s) => sum + s.hours_studied, 0);
    return { name: subject, value: subjectHours };
  }).filter(data => data.value > 0);

  const sampleData = [
    { name: 'Mathematics', value: 40 },
    { name: 'Physics', value: 25 },
    { name: 'Chemistry', value: 20 },
    { name: 'Biology', value: 15 }
  ];

  const colors = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="dashboard-container">
      <Navigation />

      <div className="dashboard-content">
        <div className="dashboard-header">
          <h2>📊 Study Dashboard</h2>
          <p>Track your learning progress and achievements</p>
        </div>

        <div className="dashboard-tabs">
          <button
            className={`tab-btn ${activePage === 'overview' ? 'active' : ''}`}
            onClick={() => setActivePage('overview')}
          >
            📈 Overview
          </button>
          <button
            className={`tab-btn ${activePage === 'addSession' ? 'active' : ''}`}
            onClick={() => setActivePage('addSession')}
          >
            ✏️ Add Session
          </button>
          <button
            className={`tab-btn ${activePage === 'analytics' ? 'active' : ''}`}
            onClick={() => setActivePage('analytics')}
          >
            📊 Analytics
          </button>
        </div>

        {/* Overview Page */}
        {activePage === 'overview' && (
          <div className="dashboard-page">
            {/* Stats Cards */}
            <div className="stats-grid">
              <div className="stat-card">
                <div className="stat-icon">⏱️</div>
                <div className="stat-content">
                  <p className="stat-label">Total Hours This Week</p>
                  <p className="stat-value">{stats.totalHours}h</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">📚</div>
                <div className="stat-content">
                  <p className="stat-label">Study Sessions</p>
                  <p className="stat-value">{stats.totalSessions}</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">⭐</div>
                <div className="stat-content">
                  <p className="stat-label">Avg. Productivity</p>
                  <p className="stat-value">{stats.avgProductivity}/5</p>
                </div>
              </div>

              <div className="stat-card">
                <div className="stat-icon">🎯</div>
                <div className="stat-content">
                  <p className="stat-label">Subjects</p>
                  <p className="stat-value">{subjects.length}</p>
                </div>
              </div>
            </div>

            {/* Today's Sessions */}
            <div className="card">
              <h3>📅 Today's Sessions</h3>
{todaySessions.length > 0 ? (
                <div className="sessions-list">
                  {todaySessions.map((session, idx) => {
                    const minutes = session.hours_studied * 60;
                    let status = 'Average';
                    let statusColor = 'orange';
                    if (minutes > 40) {
                      status = 'Productive';
                      statusColor = 'green';
                    } else if (minutes < 20) {
                      status = 'Unproductive';
                      statusColor = 'red';
                    }
                    return (
                      <div key={idx} className="session-item">
                        <div className="session-info">
                          <h4>{session.subject}</h4>
                          <p className="session-time">
                            {session.session_time} • {session.hours_studied.toFixed(1)}h ({(minutes).toFixed(0)}min)
                          </p>
                          {session.notes && <p className="session-notes">{session.notes}</p>}
                        </div>
                        <div className="session-productivity">
                          <span className="productivity-badge" style={{backgroundColor: statusColor}}>
                            {status}
                          </span>
                          <span className="productivity-stars">
                            {'⭐'.repeat(session.productivity_level)}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="no-data">No sessions logged today</p>
              )}
            </div>

            {/* Weekly Heatmap */}
            <div className="card">
              <h3>🔥 Weekly Study Heatmap</h3>
              <div className="heatmap-container">
                {['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map((day, idx) => {
                  const dayDate = new Date();
                  dayDate.setDate(dayDate.getDate() - dayDate.getDay() + idx + 1);
                  const dateStr = dayDate.toISOString().split('T')[0];
                  const daySessions = weekSessions.filter(s => s.session_date === dateStr);
                  const hours = daySessions.reduce((sum, s) => sum + s.hours_studied, 0);
                  
                  const intensity = hours === 0 ? 0 : Math.min(hours / 8, 1);
                  const color = intensity === 0 ? '#e0e0e0' : `hsl(265, ${70 + intensity * 20}%, ${50 - intensity * 15}%)`;
                  
                  return (
                    <div key={day} className="heatmap-cell" style={{ backgroundColor: color }}>
                      <div className="heatmap-day">{day}</div>
                      <div className="heatmap-hours">{hours.toFixed(1)}h</div>
                    </div>
                  );
                })}
              </div>
              <div className="heatmap-legend">
                <span>Low</span>
                <div className="legend-bar">
                  <div style={{ backgroundColor: '#e0e0e0' }}></div>
                  <div style={{ backgroundColor: '#c5b3e8' }}></div>
                  <div style={{ backgroundColor: '#9a7bd2' }}></div>
                  <div style={{ backgroundColor: '#6f5fbc' }}></div>
                  <div style={{ backgroundColor: '#4443a6' }}></div>
                </div>
                <span>High</span>
              </div>
            </div>

            {/* Weekly Summary */}
{weeklyReport && (
              <div className="card">
                <h3>📊 Weekly Summary (ML Predicted)</h3>
                <div className="readiness-report">
                  <div className="readiness-score">
                    <span className="score-label">Exam Readiness:</span>
                    <span className="score-value">{weeklyReport.exam_readiness_score || 0}%</span>
                  </div>
                  <div className="status-section">
                    <span className="status-label">Status:</span>
                    <span className="status-value">Almost Ready</span>
                  </div>
                </div>
                <div className="summary-stats">
                  Sessions: {weeklyReport.total_sessions || 0} • 
                  Avg Productivity: {weeklyReport.avg_productivity?.toFixed(1) || '0.0'}/5
                </div>
                {weeklyReport.recommendations && weeklyReport.recommendations.length > 0 && (
                  <div className="recommendations">
                    <h4>💡 Recommendations</h4>
                    <ul>
                      {weeklyReport.recommendations.slice(0, 2).map((rec, idx) => (
                        <li key={idx}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ) || (
              <div className="card">
                <h3>📊 Get Started</h3>
                <p>Log your first study session to see ML predictions!</p>
              </div>
            )}

            {/* Next Day Timetable */}
            <div className="card">
              <h3>📅 Tomorrow's Recommended Timetable</h3>
              <button onClick={fetchNextDayTimetable} className="btn btn-secondary mb-3">
                Generate Next Day Plan
              </button>
              {nextDayTimetable && (
                <div className="timetable">
                  {nextDayTimetable.timetable && nextDayTimetable.timetable.map((slot, idx) => (
                    <div key={idx} className="timetable-slot">
                      <span className="time">{slot.time}</span>
                      <span className="subject">{slot.subject}</span>
                      <span className="duration">{slot.duration}</span>
                    </div>
                  ))}
                  {nextDayTimetable.recommendations && (
                    <div className="timetable-tips">
                      <h4>Tips:</h4>
                      <ul>
                        {nextDayTimetable.recommendations.map((tip, idx) => (
                          <li key={idx}>{tip}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Add Session Page */}
        {activePage === 'addSession' && (
          <div className="dashboard-page">
            <div className="card form-card">
              <h3>📝 Log New Study Session</h3>

              {message && <div className="alert alert-success">{message}</div>}
              {error && <div className="alert alert-danger">{error}</div>}

              <form onSubmit={handleAddSession} className="session-form">
                <div className="input-group">
<label>📅 {newSession.session_date}</label>
                  <input
                    type="date"
                    name="session_date"
                    value={newSession.session_date}
                    readOnly
                    style={{ pointerEvents: 'none', backgroundColor: '#f5f5f5', opacity: 0.7 }}
                    hidden
                  />
                </div>

                <div className="input-group">
                  <label>Subject *</label>
                  <input
                    type="text"
                    name="subject"
                    value={newSession.subject}
                    onChange={handleSessionChange}
                    placeholder="Enter subject name (e.g., Mathematics, Physics, etc.)"
                  />
                </div>

                <div className="input-group">
                  <label>Hours Studied *</label>
                  <input
                    type="number"
                    name="hours_studied"
                    value={newSession.hours_studied}
                    onChange={handleSessionChange}
                    placeholder="e.g., 2.5"
                    min="0.5"
                    max="24"
                    step="0.5"
                  />
                </div>

                {/* Productivity auto-predicted by ML - hidden */}
                <input type="hidden" name="productivity_level" value={3} />

                <div className="input-group">
                  <label>Notes</label>
                  <textarea
                    name="notes"
                    value={newSession.notes}
                    onChange={handleSessionChange}
                    placeholder="Add any notes about your session..."
                  />
                </div>

                <button type="submit" className="btn btn-primary" disabled={loading}>
                  {loading ? 'Adding Session...' : '✅ Log Session'}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Analytics Page */}
{activePage === 'analytics' && (
          <div className="dashboard-page">
            <div className="card">
              <h3>📊 Subject Performance</h3>
              {subjects.length > 0 ? (
                <div className="performance-grid">
                  {subjects.map((subject) => {
                    const subjectSessions = weekSessions.filter((s) => s.subject === subject);
                    const hours = subjectSessions.reduce((sum, s) => sum + s.hours_studied, 0);
                    const avgProductivity = (
                      subjectSessions.reduce((sum, s) => sum + s.productivity_level, 0) /
                      subjectSessions.length
                    ).toFixed(1);

                    return (
                      <div key={subject} className="subject-card">
                        <h4>{subject}</h4>
                        <div className="subject-stat">
                          <span className="label">Hours</span>
                          <span className="value">{hours.toFixed(1)}h</span>
                        </div>
                        <div className="subject-stat">
                          <span className="label">Sessions</span>
                          <span className="value">{subjectSessions.length}</span>
                        </div>
                        <div className="subject-stat">
                          <span className="label">Productivity</span>
                          <span className="value">{avgProductivity}⭐</span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              ) : (
                <p className="no-data">No data available. Start logging sessions!</p>
              )}
            </div>

            {/* Subject Hours Pie Chart */}
            <div className="card">
              <h3>📈 Subject Hours Distribution</h3>
              <div className="chart-container">
                {subjects.length > 0 ? (
                  <PieChart width={400} height={300}>
                    <Pie
                      data={subjectData}
                      cx="50%"
                      cy="50%"
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      nameKey="name"
                      label
                    >
                      {subjectData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                    <Legend />
                  </PieChart>
                ) : (
                  <div style={{ textAlign: 'center', padding: '40px' }}>
                    <h4>Sample Subject Distribution</h4>
                    <PieChart width={400} height={300}>
                      <Pie
                        data={sampleData}
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        nameKey="name"
                        label
                      >
                        {sampleData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </div>
                )}
              </div>
            </div>

            <div className="card">
              <h3>📈 Weekly Trends</h3>
              <div className="trend-info">
                <p>📚 <strong>Total Sessions:</strong> {stats.totalSessions}</p>
                <p>⏱️ <strong>Total Hours:</strong> {stats.totalHours}h</p>
                <p>⭐ <strong>Avg Productivity:</strong> {stats.avgProductivity}/5</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
