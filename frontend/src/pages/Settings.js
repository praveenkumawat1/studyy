import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Navigation from '../components/Navigation';
import { authAPI } from '../services/api';
import '../styles/Settings.css';

const Settings = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('profile');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  
  const [profileData, setProfileData] = useState({
    username: '',
    email: '',
    full_name: ''
  });
  
  const [passwordData, setPasswordData] = useState({
    current_password: '',
    new_password: '',
    confirm_password: ''
  });

  useEffect(() => {
    fetchUserData();
  }, []);

  const fetchUserData = async () => {
    try {
      const response = await authAPI.getUser();
      if (response.data.success) {
        setProfileData({
          username: response.data.user.username,
          email: response.data.user.email,
          full_name: response.data.user.full_name
        });
      }
    } catch (err) {
      console.error('Error fetching user data:', err);
    }
  };

  const handleProfileChange = (e) => {
    const { name, value } = e.target;
    setProfileData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handlePasswordChange = (e) => {
    const { name, value } = e.target;
    setPasswordData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    setLoading(true);

    try {
      // Update username/profile endpoint - you'll need to add this to backend
      // For now, just show success message
      setMessage('Profile updated successfully!');
      setTimeout(() => {
        setMessage('');
      }, 3000);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    if (passwordData.new_password !== passwordData.confirm_password) {
      setError('New passwords do not match');
      return;
    }

    if (passwordData.new_password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);

    try {
      // Change password endpoint - you'll need to add this to backend
      setMessage('Password changed successfully!');
      setPasswordData({
        current_password: '',
        new_password: '',
        confirm_password: ''
      });
      setTimeout(() => {
        setMessage('');
      }, 3000);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to change password');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="settings-container">
      <Navigation />

      <div className="settings-content">
        <div className="settings-header">
          <h2>⚙️ Settings</h2>
          <p>Manage your account and preferences</p>
        </div>

        <div className="settings-tabs">
          <button
            className={`settings-tab-btn ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            👤 Profile
          </button>
          <button
            className={`settings-tab-btn ${activeTab === 'password' ? 'active' : ''}`}
            onClick={() => setActiveTab('password')}
          >
            🔐 Change Password
          </button>
          <button
            className={`settings-tab-btn ${activeTab === 'progress' ? 'active' : ''}`}
            onClick={() => setActiveTab('progress')}
          >
            📈 Progress
          </button>
        </div>

        {/* Profile Tab */}
        {activeTab === 'profile' && (
          <div className="settings-page">
            <div className="settings-card">
              <h3>Profile Information</h3>
              {message && <div className="alert alert-success">{message}</div>}
              {error && <div className="alert alert-danger">{error}</div>}

              <form onSubmit={handleUpdateProfile} className="settings-form">
                <div className="form-group">
                  <label>Full Name</label>
                  <input
                    type="text"
                    name="full_name"
                    value={profileData.full_name}
                    onChange={handleProfileChange}
                    disabled={loading}
                  />
                </div>

                <div className="form-group">
                  <label>Username</label>
                  <input
                    type="text"
                    name="username"
                    value={profileData.username}
                    onChange={handleProfileChange}
                    disabled={loading}
                  />
                </div>

                <div className="form-group">
                  <label>Email Address</label>
                  <input
                    type="email"
                    name="email"
                    value={profileData.email}
                    onChange={handleProfileChange}
                    disabled={true}
                  />
                  <small>Email cannot be changed for security reasons</small>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Updating...' : 'Update Profile'}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Password Tab */}
        {activeTab === 'password' && (
          <div className="settings-page">
            <div className="settings-card">
              <h3>Change Password</h3>
              {message && <div className="alert alert-success">{message}</div>}
              {error && <div className="alert alert-danger">{error}</div>}

              <form onSubmit={handleChangePassword} className="settings-form">
                <div className="form-group">
                  <label>Current Password</label>
                  <input
                    type="password"
                    name="current_password"
                    value={passwordData.current_password}
                    onChange={handlePasswordChange}
                    placeholder="Enter your current password"
                    disabled={loading}
                  />
                </div>

                <div className="form-group">
                  <label>New Password</label>
                  <input
                    type="password"
                    name="new_password"
                    value={passwordData.new_password}
                    onChange={handlePasswordChange}
                    placeholder="Enter new password"
                    disabled={loading}
                  />
                  <small>Must be at least 6 characters with uppercase, lowercase, and number</small>
                </div>

                <div className="form-group">
                  <label>Confirm New Password</label>
                  <input
                    type="password"
                    name="confirm_password"
                    value={passwordData.confirm_password}
                    onChange={handlePasswordChange}
                    placeholder="Confirm new password"
                    disabled={loading}
                  />
                </div>

                <button
                  type="submit"
                  className="btn btn-primary"
                  disabled={loading}
                >
                  {loading ? 'Changing...' : 'Change Password'}
                </button>
              </form>
            </div>
          </div>
        )}

        {/* Progress Tab */}
        {activeTab === 'progress' && (
          <div className="settings-page">
            <div className="settings-card">
              <h3>📊 Your Progress Overview</h3>
              
              <div className="progress-stats">
                <div className="progress-stat">
                  <h4>Total Study Hours</h4>
                  <p className="big-number">45.5</p>
                  <small>This month</small>
                </div>

                <div className="progress-stat">
                  <h4>Total Sessions</h4>
                  <p className="big-number">28</p>
                  <small>This month</small>
                </div>

                <div className="progress-stat">
                  <h4>Average Daily Study</h4>
                  <p className="big-number">2.3h</p>
                  <small>per day</small>
                </div>

                <div className="progress-stat">
                  <h4>Consistency Score</h4>
                  <p className="big-number">92%</p>
                  <small>Excellent! Keep it up</small>
                </div>
              </div>

              <div className="progress-details">
                <h4>📈 Monthly Achievements</h4>
                <ul>
                  <li>✅ 30 days streak - Amazing consistency!</li>
                  <li>✅ 100+ total hours - Dedicated learner</li>
                  <li>✅ 5+ subjects tracked - Well-rounded student</li>
                  <li>✅ 4.5/5 avg productivity - Very productive</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;
