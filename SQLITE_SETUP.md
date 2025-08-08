# SQLite + SQLAlchemy Backend Setup Guide

## 🔄 Migration from Supabase to SQLite

This guide walks you through setting up the new SQLite-based backend with SQLAlchemy instead of Supabase.

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- A modern web browser

## 🚀 Quick Setup

### 1. Install Dependencies

Navigate to the backend directory and install the required packages:

```bash
cd backend
pip install -r requirements_sqlite.txt
```

### 2. Initialize Database

Run the database initialization script to create tables and add sample data:

```bash
python init_database.py
```

This will:
- Create a SQLite database file `school.db`
- Create all necessary tables
- Add sample data (news, events, results, faculty, toppers)
- Create an admin user with credentials: `admin` / `admin123`

### 3. Start the Backend Server

```bash
python app_sqlite.py
```

The server will start on `http://localhost:5000`

### 4. Update Frontend

Update the admin login page to use the new JWT authentication:
- Replace `frontend/admin/login.html` with `frontend/admin/login_jwt.html`
- Or rename the files:
  ```bash
  cd frontend/admin
  move login.html login_supabase.html
  move login_jwt.html login.html
  ```

## 📁 File Structure

```
backend/
├── app_sqlite.py              # New SQLite Flask application
├── app.py                     # Original Supabase application (backup)
├── requirements_sqlite.txt    # SQLite dependencies
├── init_database.py          # Database initialization script
├── school.db                 # SQLite database file (created after init)
└── uploads/                  # File upload directory

frontend/
├── admin/
│   ├── login_jwt.html        # New JWT-based login page
│   └── login.html            # Original Supabase login (backup)
├── css/styles.css            # Updated styles
├── js/app.js                 # Updated to use SQLite API
└── index.html                # Updated with new design
```

## 🔐 Authentication

### Admin Login
- **URL**: `http://localhost:3000/admin/login.html` (or your frontend URL)
- **Username**: `admin`
- **Password**: `admin123`

### JWT Tokens
- Tokens expire after 24 hours
- Stored in browser localStorage as `admin_token`
- Auto-refresh on backend API calls

## 📊 Database Schema

### Tables Created:
- **admins** - Admin users with password hashing
- **news** - News and announcements
- **admissions** - Student admission applications
- **contact_messages** - Contact form submissions
- **events** - School events and activities
- **results** - Academic results by class and year
- **toppers** - Student toppers with achievements
- **gallery** - Image gallery with categories
- **faculty** - Faculty member profiles

## 🔧 API Endpoints

### Public Endpoints (No Auth Required)
```
GET  /api/health           # Health check
GET  /api/news             # Get latest news
POST /api/admissions       # Submit admission application
POST /api/contact          # Submit contact message
GET  /api/events           # Get events
GET  /api/results          # Get results data
GET  /api/gallery          # Get gallery images
GET  /api/faculty          # Get faculty members
GET  /api/uploads/<file>   # Serve uploaded files
```

### Admin Endpoints (JWT Auth Required)
```
POST /api/auth/login       # Admin login
GET  /api/auth/me          # Get current admin info
POST /api/news             # Create news item
GET  /api/admissions       # Get admission applications
PUT  /api/admissions/<id>/status  # Update admission status
GET  /api/contact          # Get contact messages
POST /api/events           # Create event
POST /api/results          # Create result entry
POST /api/gallery          # Upload gallery image
POST /api/faculty          # Create faculty member
GET  /api/dashboard/stats  # Get dashboard statistics
```

## 🛠️ Configuration

### Environment Variables
You can set these in your environment or modify the defaults in `app_sqlite.py`:

```bash
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=sqlite:///school.db
JWT_SECRET_KEY=jwt-secret-string
FLASK_ENV=development
PORT=5000
```

### Database Configuration
- **Database**: SQLite file (`school.db`)
- **Location**: Same directory as `app_sqlite.py`
- **Backup**: Automatically created on first run

## 📝 Key Differences from Supabase Version

### ✅ Advantages of SQLite Version:
1. **No External Dependencies** - Everything runs locally
2. **Simpler Setup** - No need to configure Supabase account
3. **File-based Database** - Easy to backup and move
4. **JWT Authentication** - Standard token-based auth
5. **Local File Uploads** - Files stored in `uploads/` directory
6. **Full Control** - Complete control over database and authentication

### ⚠️ Considerations:
1. **Single File Database** - Not suitable for high-concurrency production
2. **Local Storage** - Files are stored locally, not in cloud
3. **Manual Scaling** - Need to handle scaling manually
4. **Backup Strategy** - Need to implement your own backup solution

## 🧪 Testing the Setup

1. **Test Backend Health**:
   ```bash
   curl http://localhost:5000/api/health
   ```

2. **Test Admin Login**:
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
        -H "Content-Type: application/json" \
        -d '{"username":"admin","password":"admin123"}'
   ```

3. **Test Public Endpoints**:
   ```bash
   curl http://localhost:5000/api/news
   curl http://localhost:5000/api/events
   curl http://localhost:5000/api/results
   ```

## 🔄 Database Management

### Reset Database
To completely reset the database with fresh sample data:
```bash
python init_database.py --reset
```

### Backup Database
```bash
cp school.db school_backup_$(date +%Y%m%d).db
```

### View Database Contents
You can use any SQLite browser or command line:
```bash
sqlite3 school.db
.tables
SELECT * FROM news;
.quit
```

## 🚀 Production Deployment

For production deployment:

1. **Change Default Passwords**:
   ```python
   admin.set_password('your-secure-password')
   ```

2. **Set Environment Variables**:
   ```bash
   export SECRET_KEY='your-production-secret-key'
   export JWT_SECRET_KEY='your-jwt-secret'
   export FLASK_ENV='production'
   ```

3. **Use a Process Manager** (e.g., Gunicorn):
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app_sqlite:app
   ```

4. **Set up Reverse Proxy** (e.g., Nginx)

5. **Implement Database Backups**:
   ```bash
   # Daily backup script
   cp school.db backups/school_$(date +%Y%m%d).db
   ```

## 🐛 Troubleshooting

### Common Issues:

1. **ModuleNotFoundError**:
   ```bash
   pip install -r requirements_sqlite.txt
   ```

2. **Database locked error**:
   - Make sure only one Flask instance is running
   - Check file permissions on `school.db`

3. **CORS errors**:
   - Check CORS origins in `app_sqlite.py`
   - Add your frontend URL to the allowed origins

4. **Token expired**:
   - Tokens expire after 24 hours
   - Login again to get a new token

### Debug Mode:
Run with debug enabled:
```bash
FLASK_ENV=development python app_sqlite.py
```

## 📚 Sample Data Included

The initialization script creates sample data for:
- 4 news items
- 4 events (sports day, science exhibition, etc.)
- Academic results for Class X and XII (2022-2024)
- 5 student toppers
- 6 faculty members (including principal)
- 1 admin user

## 🔮 Next Steps

1. **Create Admin Dashboard** - Build a full admin interface
2. **Add Email Notifications** - Send emails for admissions/contact
3. **File Upload Interface** - Admin interface for gallery uploads
4. **Database Migrations** - Version control for database schema
5. **API Documentation** - Generate Swagger/OpenAPI docs
6. **Unit Tests** - Add comprehensive test suite

---

## 🎉 Success!

You now have a fully functional SQLite-based backend for the Shri Shyam Public School website! 

The system is now completely self-contained and doesn't require any external services like Supabase. All data is stored locally in the SQLite database, and authentication is handled with JWT tokens.

**Admin Access**: `http://localhost:3000/admin/login.html`
**API Base**: `http://localhost:5000/api`

Happy coding! 🚀
