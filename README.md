# Shri Shyam Public School Website

A complete full-stack school website for "Shri Shyam Public School, Kushalpura" featuring a modern responsive frontend, Flask REST API backend, and SQLite database.

## 🎯 Features

### Public Website
- **Responsive Design**: Mobile-first approach with modern UI
- **Multi-language Support**: English and Hindi toggle
- **Hero Section**: Image slider with school highlights
- **News Ticker**: Latest announcements and achievements
- **Complete Sections**: Home, About, Academics, Facilities, Admissions, Results, Events, Faculty, Contact
- **Interactive Forms**: Online admission applications and contact forms
- **Gallery**: Photo lightbox with categorized images
- **Results Display**: Academic performance tables and topper showcases

### Admin Dashboard
- **Secure Authentication**: JWT-based login system
- **Content Management**: Manage news, events, results, and gallery
- **Application Management**: View and process admission applications
- **Message Center**: Handle contact form submissions
- **File Upload**: Local image storage with organized structure

### Technical Features
- **REST API**: Complete Flask backend with JWT authentication
- **Database**: SQLite with SQLAlchemy ORM
- **File Storage**: Local file system storage
- **Self-contained**: No external dependencies
- **SEO Optimized**: Proper meta tags and semantic HTML

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Custom styles with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Libraries**: Font Awesome icons, Google Fonts

### Backend
- **Python Flask**: RESTful API server
- **SQLAlchemy**: Database ORM and migrations
- **Flask-JWT-Extended**: JWT token authentication
- **Flask-CORS**: Cross-origin request handling
- **Flask-Bcrypt**: Password hashing

### Database
- **SQLite**: File-based database
- **SQLAlchemy Models**: Structured database schema
- **Local Storage**: File uploads stored locally

## 📁 Project Structure

```
shri-shyam-school/
├── frontend/
│   ├── index.html              # Main homepage
│   ├── css/
│   │   └── styles.css         # Complete CSS styles
│   ├── js/
│   │   └── app.js             # JavaScript functionality
│   ├── images/                # Image assets
│   └── admin/
│       └── login.html         # JWT-based admin login
├── backend/
│   ├── app.py                 # Flask SQLite application
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   ├── init_database.py      # Database initialization
│   ├── school.db             # SQLite database (created on init)
│   └── uploads/              # Local file storage
├── docs/
│   └── README.md             # This file
└── SQLITE_SETUP.md          # Detailed setup guide
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd shri-shyam-school
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database with sample data
python init_database.py

# Run the Flask app
python app.py
```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

```bash
cd frontend

# For development, you can use Python's built-in server
python -m http.server 8000

# Or use Live Server extension in VS Code
# Or any other static file server
```

The frontend will be available at `http://localhost:8000`

### 4. Admin Access

**Default admin credentials:**
- **Username**: `admin`
- **Password**: `admin123`
- **Login URL**: `http://localhost:8000/admin/login.html`

⚠️ **Remember to change the default password in production!**

## 📊 Database Schema

The SQLite database includes the following tables:

- **admins**: Admin users with hashed passwords
- **news**: Announcements and news items
- **admissions**: Student admission applications
- **contact_messages**: Contact form submissions
- **events**: School events and activities
- **results**: Academic results by class and year
- **toppers**: Academic toppers information
- **gallery**: Photo gallery with categories
- **faculty**: Faculty member profiles

## 🔧 Configuration

### Environment Variables (.env)

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key

# Database Configuration
DATABASE_URL=sqlite:///school.db

# JWT Configuration
JWT_SECRET_KEY=your-jwt-secret-key

# Optional configurations
PORT=5000
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

### Frontend Configuration

Update the API base URL in `js/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
```

## 🌐 API Endpoints

### Public Endpoints
- `GET /api/health` - Health check
- `GET /api/news` - Get latest news
- `POST /api/admissions` - Submit admission application
- `POST /api/contact` - Submit contact message
- `GET /api/events` - Get events
- `GET /api/results` - Get academic results
- `GET /api/gallery` - Get gallery images
- `GET /api/faculty` - Get faculty information
- `GET /api/uploads/<file>` - Serve uploaded files

### Admin Endpoints (JWT Authentication Required)
- `POST /api/auth/login` - Admin login
- `GET /api/auth/me` - Get current admin info
- `POST /api/news` - Create news item
- `GET /api/admissions` - Get admission applications
- `PUT /api/admissions/<id>/status` - Update application status
- `GET /api/contact` - Get contact messages
- `POST /api/events` - Create event
- `POST /api/results` - Create result entry
- `POST /api/gallery` - Upload gallery image
- `POST /api/faculty` - Create faculty member
- `GET /api/dashboard/stats` - Get dashboard statistics

## 🎨 Customization

### Branding
1. Replace logo in `frontend/images/logo.png`
2. Update school information in HTML files
3. Modify color scheme in CSS variables
4. Update contact information and addresses

### Content
1. Modify sample data in `init_database.py`
2. Update faculty information
3. Add school-specific images
4. Customize text content and descriptions

### Database
```bash
# Reset database with fresh sample data
python init_database.py --reset

# Backup database
cp school.db school_backup_$(date +%Y%m%d).db
```

## 📱 Responsive Design

The website is fully responsive with breakpoints:
- Desktop: 1200px+
- Tablet: 768px - 1199px
- Mobile: 320px - 767px

Key responsive features:
- Mobile-first CSS approach
- Flexible grid layouts
- Touch-friendly interface
- Optimized images
- Collapsible navigation

## 🔒 Security Features

- JWT token authentication
- Password hashing with bcrypt
- Input validation and sanitization
- CORS configuration
- SQL injection prevention via SQLAlchemy
- XSS protection
- Secure file upload handling

## 🚀 Deployment

### Frontend Deployment (Netlify/Vercel)

1. Deploy the frontend folder to any static hosting service
2. Update `API_BASE_URL` in `js/app.js` to your backend URL

### Backend Deployment (Railway/Render/Heroku)

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Set environment variables:
```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
CORS_ORIGINS=https://your-frontend-domain.com
```

3. Deploy with database initialization:
```bash
python init_database.py
```

## 🧪 Testing

Test the setup with these commands:

```bash
# Health check
curl http://localhost:5000/api/health

# Test login
curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"admin123"}'

# Test public endpoints
curl http://localhost:5000/api/news
curl http://localhost:5000/api/events
```

## 📖 User Guide

### For Administrators

1. **Login**: Access admin panel at `/admin/login.html`
2. **Dashboard**: View statistics and manage content
3. **News Management**: Add/edit announcements
4. **Admission Applications**: Review and process applications
5. **Contact Messages**: Respond to inquiries
6. **Gallery**: Upload and organize photos
7. **Events**: Create and manage school events

### For Website Visitors

1. **Browse Information**: Explore school sections
2. **Apply Online**: Fill admission application
3. **Contact School**: Use contact form
4. **View Results**: Check academic performance
5. **Gallery**: Browse school photos
6. **Events**: Stay updated with activities

## 🔧 Troubleshooting

### Common Issues

**1. Database errors**
- Check if `school.db` file exists
- Run `python init_database.py` to create database
- Verify file permissions

**2. Frontend not loading data**
- Check `API_BASE_URL` in `app.js`
- Verify CORS configuration in Flask app
- Check browser console for errors

**3. Admin login not working**
- Verify JWT secret key is set
- Check admin credentials (default: admin/admin123)
- Ensure token is being stored in localStorage

**4. File upload issues**
- Check `uploads/` directory exists and is writable
- Verify file size limits
- Check allowed file extensions

### Debug Mode

Enable debug mode in Flask:
```bash
FLASK_ENV=development python app.py
```

## ✅ Advantages of SQLite Version

1. **No External Dependencies** - Everything runs locally
2. **Simpler Setup** - No cloud account needed
3. **File-based Database** - Easy to backup and move
4. **JWT Authentication** - Standard token-based auth
5. **Local File Uploads** - Files stored in `uploads/` directory
6. **Full Control** - Complete control over database and authentication
7. **Development Friendly** - Perfect for development and small deployments

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support or questions:
- Check `SQLITE_SETUP.md` for detailed setup instructions
- Create an issue on GitHub
- Review troubleshooting section above

## 🙏 Acknowledgments

- Flask community for the excellent framework
- SQLAlchemy for the robust ORM
- Font Awesome for icons
- Google Fonts for typography

---

Built with ❤️ for Shri Shyam Public School, Kushalpura

🎉 **Now completely free from external dependencies!**
# ssps
