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
- **Secure Authentication**: Supabase-powered login system
- **Content Management**: Manage news, events, results, and gallery
- **Application Management**: View and process admission applications
- **Message Center**: Handle contact form submissions
- **File Upload**: Image management with Supabase Storage

### Technical Features
- **REST API**: Complete Flask backend with JWT authentication
- **Database**: PostgreSQL via Supabase with Row Level Security
- **File Storage**: Supabase Storage for images and documents
- **Real-time Updates**: Live data synchronization
- **SEO Optimized**: Proper meta tags and semantic HTML

## 🛠️ Technology Stack

### Frontend
- **HTML5**: Semantic markup with accessibility features
- **CSS3**: Custom styles with CSS Grid and Flexbox
- **JavaScript**: Vanilla JS with modern ES6+ features
- **Libraries**: Font Awesome icons, Google Fonts

### Backend
- **Python Flask**: RESTful API server
- **Supabase**: PostgreSQL database and authentication
- **Flask-CORS**: Cross-origin request handling
- **JWT**: Token-based authentication

### Database
- **Supabase PostgreSQL**: Cloud-hosted PostgreSQL
- **Row Level Security**: Secure data access
- **Real-time**: Live data synchronization

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
│       └── login.html         # Admin login page
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── supabase_schema.sql   # Database schema
├── docs/
│   └── README.md             # This file
└── sample-data/              # Sample data files
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js (optional, for development server)
- Supabase account
- Git

### 1. Clone the Repository
```bash
git clone <repository-url>
cd shri-shyam-school
```

### 2. Set Up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to Settings → API to get your project URL and API keys
3. In the SQL Editor, run the schema from `backend/supabase_schema.sql`
4. Create storage buckets:
   - Go to Storage → Create bucket: `gallery` (public)
   - Create bucket: `faculty-photos` (public)
   - Create bucket: `documents` (public)

### 3. Backend Setup

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

# Create environment file
cp .env.example .env

# Edit .env with your Supabase credentials
# SUPABASE_URL=your_supabase_url
# SUPABASE_KEY=your_supabase_anon_key
# SECRET_KEY=your_secret_key

# Run the Flask app
python app.py
```

The backend will be available at `http://localhost:5000`

### 4. Frontend Setup

```bash
cd frontend

# For development, you can use Python's built-in server
python -m http.server 8000

# Or use Live Server extension in VS Code
# Or any other static file server
```

The frontend will be available at `http://localhost:8000`

### 5. Create Admin User

In your Supabase dashboard:
1. Go to Authentication → Users
2. Click "Add user"
3. Enter email and password for admin access
4. The user can now login at `/admin/login.html`

## 📊 Database Schema

The database includes the following main tables:

- **news**: Announcements and news items
- **admissions**: Student admission applications
- **contact_messages**: Contact form submissions
- **events**: School events and activities
- **results**: Academic results by class and year
- **toppers**: Academic toppers information
- **gallery**: Photo gallery with categories
- **faculty**: Faculty member profiles
- **settings**: Website configuration

## 🔧 Configuration

### Environment Variables (.env)

```env
# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-super-secret-key

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key

# Optional configurations
PORT=5000
CORS_ORIGINS=http://localhost:3000,https://your-domain.com
```

### Frontend Configuration

Update the following variables in `js/app.js`:

```javascript
const API_BASE_URL = 'http://localhost:5000/api';
const SUPABASE_URL = 'your-supabase-url';
const SUPABASE_ANON_KEY = 'your-supabase-anon-key';
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

### Admin Endpoints (Authenticated)
- `POST /api/news` - Create news item
- `GET /api/admissions` - Get admission applications
- `PUT /api/admissions/:id/status` - Update application status
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
1. Modify sample data in `supabase_schema.sql`
2. Update faculty information
3. Add school-specific images
4. Customize text content and descriptions

### Styling
The CSS uses custom properties for easy theming:

```css
:root {
  --primary-color: #FF6B35;
  --secondary-color: #F7931E;
  --text-color: #333;
  --bg-color: #f8f9fa;
}
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

- Row Level Security (RLS) policies
- JWT token authentication
- Input validation and sanitization
- CORS configuration
- SQL injection prevention
- XSS protection

## 🚀 Deployment

### Frontend Deployment (Netlify/Vercel)

1. Build the frontend:
```bash
# No build process needed for vanilla HTML/CSS/JS
# Just deploy the frontend folder
```

2. Deploy to Netlify:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod --dir .
```

3. Update API_BASE_URL in `js/app.js` to your backend URL

### Backend Deployment (Render/Railway/Heroku)

1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy to Render:
   - Connect your GitHub repository
   - Set environment variables
   - Deploy from `backend` directory

3. Update CORS origins with your frontend URL

### Environment Variables for Production

```env
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-anon-key
SUPABASE_SERVICE_KEY=your-supabase-service-key
CORS_ORIGINS=https://your-frontend-domain.com
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

**1. Backend not connecting to Supabase**
- Check environment variables
- Verify Supabase credentials
- Ensure RLS policies are set correctly

**2. Frontend not loading data**
- Check API_BASE_URL in app.js
- Verify CORS configuration
- Check browser console for errors

**3. Admin login not working**
- Ensure Supabase auth is configured
- Check user exists in Supabase dashboard
- Verify authentication flow

**4. Images not uploading**
- Check Supabase storage buckets exist
- Verify storage policies
- Check file size limits

### Debug Mode

Enable debug mode in Flask:
```python
app.run(debug=True)
```

Check browser developer tools for JavaScript errors.

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
- Create an issue on GitHub
- Email: support@example.com

## 🙏 Acknowledgments

- Supabase for database and authentication
- Font Awesome for icons
- Google Fonts for typography
- Flask community for the framework

---

Built with ❤️ for Shri Shyam Public School, Kushalpura
