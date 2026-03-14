import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/Navigation.css';

const Navigation = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [showDropdown, setShowDropdown] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-brand">
          <div className="navbar-logo">
            <span className="logo-icon">📚</span>
            <span className="logo-text">Study Tracker</span>
          </div>
        </div>

        <div className="navbar-right">
          <div className="welcome-message">
            Welcome, <strong>{user?.full_name || user?.username}</strong>
          </div>

          <div className="user-menu">
            <button 
              className="user-avatar"
              onClick={() => setShowDropdown(!showDropdown)}
            >
              {user?.full_name?.charAt(0)?.toUpperCase() || 'U'}
            </button>

            {showDropdown && (
              <div className="dropdown-menu">
                <div className="dropdown-header">
                  <p className="user-name">{user?.full_name || user?.username}</p>
                  <p className="user-email">{user?.email}</p>
                </div>
                <div className="dropdown-divider"></div>
                <button 
                  className="dropdown-item"
                  onClick={() => navigate('/dashboard')}
                >
                  📊 Dashboard
                </button>
                <button 
                  className="dropdown-item"
                  onClick={() => navigate('/settings')}
                >
                  ⚙️ Settings
                </button>
                <div className="dropdown-divider"></div>
                <button 
                  className="dropdown-item logout-btn"
                  onClick={handleLogout}
                >
                  🚪 Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;
