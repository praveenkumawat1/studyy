# Study Tracker Frontend

A modern, beautiful React.js frontend for the AI-powered Study Tracker application.

## Features

✨ **Modern UI Design**
- Clean and aesthetic card-based layouts
- Gradient backgrounds and smooth animations
- Fully responsive design (mobile, tablet, desktop)

🔐 **Authentication**
- User registration with email validation
- Secure login system
- Password strength validation
- Persistent user sessions

📊 **Dashboard**
- Welcome message with user name
- Statistics overview (hours, sessions, productivity)
- Today's study sessions view
- Weekly summary with exam readiness score
- Subject performance analytics
- Study trends visualization

✏️ **Study Tracking**
- Log new study sessions
- Select subjects
- Track hours studied
- Rate productivity level (1-5 stars)
- Add notes to sessions

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   └── Navigation.js       # Top navigation bar
│   ├── context/
│   │   └── AuthContext.js      # Authentication state management
│   ├── pages/
│   │   ├── Login.js            # Login page
│   │   ├── Register.js         # Registration page
│   │   └── Dashboard.js        # Main dashboard
│   ├── services/
│   │   └── api.js              # API integration
│   ├── styles/
│   │   ├── index.css           # Global styles
│   │   ├── Auth.css            # Authentication pages styles
│   │   ├── Navigation.css      # Navigation bar styles
│   │   └── Dashboard.css       # Dashboard styles
│   ├── App.js                  # Main app component with routing
│   └── index.js                # Entry point
├── package.json
└── README.md
```

## Installation

### Prerequisites
- Node.js (v14+)
- npm or yarn
- Python backend running (see main project README)

### Setup

1. **Navigate to frontend directory:**
```bash
cd frontend
```

2. **Install dependencies:**
```bash
npm install
```

3. **Start the development server:**
```bash
npm start
```

The application will open at `http://localhost:3000`

## Configuration

The frontend communicates with the backend API. Update the API base URL in `src/services/api.js` if needed:

```javascript
const api = axios.create({
  baseURL: 'http://localhost:5000/api',  // Change this if your backend runs on a different port
});
```

## Pages

### Login Page (`src/pages/Login.js`)
- Clean card UI centered on page
- Input fields: Username, Password
- Login button
- Link to registration page
- Features display (track sessions, get insights, achieve goals)

### Registration Page (`src/pages/Register.js`)
- Full name input
- Email validation
- Phone number (10 digits)
- Strong password validation (uppercase, lowercase, number)
- Confirm password matching
- Form validation with error messages

### Dashboard (`src/pages/Dashboard.js`)
- Welcome message: "Welcome, {User Name}"
- Top navigation with user menu
- Statistics cards (hours, sessions, productivity, subjects)
- Three tabs: Overview, Add Session, Analytics

#### Overview Tab
- Statistics overview
- Today's logged sessions
- Weekly summary with exam readiness score
- Personalized recommendations

#### Add Session Tab
- Form to log new study session
- Subject selection dropdown
- Hours studied input
- Productivity level slider (1-5 stars)
- Notes textarea
- Success/error messages

#### Analytics Tab
- Subject-wise performance breakdown
- Weekly trends summary
- Visual statistics

## Navigation Component

The Navigation bar includes:
- Study Tracker logo
- Welcome message with user name
- User avatar (first letter of name)
- Dropdown menu with options:
  - Dashboard
  - Settings
  - Logout

## Styling

The project uses custom CSS with:
- CSS variables for consistent theming
- Gradient backgrounds
- Smooth animations and transitions
- Mobile-responsive design
- Accessible color contrasts

### Color Scheme
- Primary: #667eea → #764ba2 (gradient)
- Success: #48bb78
- Danger: #f56565
- Warning: #ed8936
- Light Background: #f7fafc
- Dark Text: #2d3748

## State Management

Uses React Context API for:
- User authentication state
- User information storage
- Login/logout operations
- Protected routes

## API Integration

The frontend connects to the backend API endpoints:
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/sessions/today` - Today's sessions
- `GET /api/sessions/week` - Week's sessions
- `POST /api/sessions` - Add new session
- `GET /api/reports/weekly` - Weekly report

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers

## Build for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Troubleshooting

### Port 3000 already in use
```bash
PORT=3001 npm start
```

### CORS errors
Ensure the backend is running and the API base URL is correct in `src/services/api.js`

### Login not working
- Check if backend is running (`python study_tracker_app_db.py`)
- Verify credentials are correct
- Check browser console for error messages

## Future Enhancements

- Dark mode toggle
- Chart.js for data visualization
- Calendar view for study sessions
- Export reports as PDF
- Profile editing
- Study goals management
- Notifications system
- Real-time collaboration features

## License

MIT License - See LICENSE file for details

## Support

For issues or questions, refer to the main project documentation.
