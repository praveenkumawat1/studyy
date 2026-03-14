import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle responses
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Authentication endpoints
export const authAPI = {
  login: (username, password) =>
    api.post('/auth/login', { username, password }),
  
  register: (username, email, phone, password) =>
    api.post('/auth/register', { username, email, phone, password }),
  
  getCurrentUser: () =>
    api.get('/auth/user'),
};

// Study sessions endpoints
export const sessionsAPI = {
  addSession: (sessionData) =>
    api.post('/sessions', sessionData),
  
  getTodaySessions: () =>
    api.get('/sessions/today'),
  
  getWeekSessions: () =>
    api.get('/sessions/week'),
  
  getMonthSessions: () =>
    api.get('/sessions/month'),
  
  deleteSession: (sessionId) =>
    api.delete(`/sessions/${sessionId}`),
  
  getNextDayTimetable: () =>
    api.get('/timetable/next-day'),
};

// Reports endpoints
export const reportsAPI = {
  getWeeklyReport: () =>
    api.get('/reports/weekly'),
  
  getMonthlyReport: () =>
    api.get('/reports/monthly'),
};

// Timetable endpoints
export const timetableAPI = {
  generateTimetable: () =>
    api.post('/timetable/generate'),
  
  getTimetable: () =>
    api.get('/timetable/latest'),
  
  getNextDayTimetable: () =>
    api.get('/timetable/next-day'),
};

// Analytics endpoints
export const analyticsAPI = {
  getProgress: () =>
    api.get('/analytics/progress'),
  
  getSubjectPerformance: () =>
    api.get('/analytics/subjects'),
};

export default api;
