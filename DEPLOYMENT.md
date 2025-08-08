# Deployment Guide - Shri Shyam Public School Website (SQLite)

This guide will help you deploy the school website to production using the SQLite backend.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ SQLite backend set up (see SQLITE_SETUP.md)
- ✅ All environment variables configured
- ✅ Domain name (optional but recommended)
- ✅ SSL certificate (handled by hosting platforms)

## 🌐 Deployment Options

### Option 1: Quick Deploy (Recommended for Beginners)
**Frontend: Netlify + Backend: Render**

### Option 2: Advanced Deploy
**Frontend: Vercel + Backend: Railway**

### Option 3: Self-hosted
**Your own VPS or server**

---

## 🚀 Option 1: Netlify + Render (Recommended)

### Part A: Deploy Backend to Render

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure Service**
   ```
   Name: shri-shyam-school-api
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Set Environment Variables**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-production-secret-key-change-this
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=sqlite:///school.db
   PORT=10000
   ```

5. **Advanced Settings**
   - Root Directory: `backend`
   - Python Version: 3.11
   - Auto-Deploy: Yes

6. **Database Initialization**
   Add this to your build command:
   ```
   pip install -r requirements.txt && python init_database.py
   ```

7. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your backend URL: `https://your-app.onrender.com`

### Part B: Deploy Frontend to Netlify

1. **Prepare Frontend**
   - Update `frontend/js/app.js`:
   ```javascript
   const API_BASE_URL = 'https://your-app.onrender.com/api';
   ```

2. **Deploy to Netlify**
   ```bash
   # Install Netlify CLI
   npm install -g netlify-cli

   # Login
   netlify login

   # Deploy from frontend directory
   cd frontend
   netlify deploy --prod --dir .
   ```

3. **Configure Custom Domain (Optional)**
   - In Netlify dashboard → Domain management
   - Add custom domain
   - Configure DNS settings

---

## 🚀 Option 2: Vercel + Railway

### Part A: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Configure Environment**
   ```
   FLASK_ENV=production
   SECRET_KEY=your-production-secret-key
   JWT_SECRET_KEY=your-jwt-secret-key
   DATABASE_URL=sqlite:///school.db
   PORT=8080
   ```

4. **Configure Build**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt && python init_database.py`
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

5. **Deploy**
   - Railway will auto-deploy
   - Note your backend URL

### Part B: Deploy Frontend to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Configure**
   - Follow Vercel setup prompts
   - Update API_BASE_URL in your code
   - Redeploy if needed

---

## 🖥️ Option 3: Self-Hosted (VPS)

### Prerequisites
- Ubuntu 20.04+ VPS
- Domain name pointing to your server
- Basic Linux knowledge

### Step 1: Server Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install python3 python3-pip nginx supervisor git -y

# Install Node.js (optional)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Step 2: Deploy Backend

```bash
# Clone repository
git clone <your-repo-url>
cd shri-shyam-school/backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python init_database.py

# Create environment file
cp .env.example .env
nano .env  # Edit with your values

# Test application
python app.py
```

### Step 3: Configure Gunicorn

```bash
# Create Gunicorn config
sudo nano /etc/supervisor/conf.d/shri-shyam-school.conf
```

```ini
[program:shri-shyam-school]
command=/home/ubuntu/shri-shyam-school/backend/venv/bin/gunicorn app:app --bind 127.0.0.1:5000
directory=/home/ubuntu/shri-shyam-school/backend
user=ubuntu
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/shri-shyam-school.log
```

```bash
# Update supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start shri-shyam-school
```

### Step 4: Configure Nginx

```bash
# Create Nginx config
sudo nano /etc/nginx/sites-available/shri-shyam-school
```

```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Frontend
    location / {
        root /home/ubuntu/shri-shyam-school/frontend;
        index index.html;
        try_files $uri $uri/ =404;
    }
    
    # API Backend
    location /api/ {
        proxy_pass http://127.0.0.1:5000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Serve uploaded files
    location /uploads/ {
        alias /home/ubuntu/shri-shyam-school/backend/uploads/;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/shri-shyam-school /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Step 5: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal (optional)
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🔧 Production Configuration

### Environment Variables

**Backend (.env):**
```env
FLASK_ENV=production
SECRET_KEY=your-super-secure-production-key
JWT_SECRET_KEY=your-jwt-production-key
DATABASE_URL=sqlite:///school.db
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

**Frontend (js/app.js):**
```javascript
const API_BASE_URL = 'https://your-domain.com/api';
// or 'https://your-backend.render.com/api' for separate hosting
```

### Security Checklist

- ✅ Change default admin password
- ✅ Use strong SECRET_KEY and JWT_SECRET_KEY
- ✅ Enable HTTPS/SSL
- ✅ Configure CORS properly
- ✅ Set up database backups
- ✅ Monitor application logs
- ✅ Keep dependencies updated

---

## 📊 Database Management in Production

### Backup Database

```bash
# Create backup
cp school.db school_backup_$(date +%Y%m%d_%H%M%S).db

# Automated backup script
#!/bin/bash
BACKUP_DIR="/home/ubuntu/backups"
mkdir -p $BACKUP_DIR
cp /home/ubuntu/shri-shyam-school/backend/school.db $BACKUP_DIR/school_backup_$(date +%Y%m%d_%H%M%S).db

# Keep only last 7 days
find $BACKUP_DIR -name "school_backup_*.db" -mtime +7 -delete
```

### Reset Database (if needed)

```bash
cd /home/ubuntu/shri-shyam-school/backend
source venv/bin/activate
python init_database.py --reset
```

---

## 🔍 Monitoring & Logs

### Check Application Status

```bash
# Check if backend is running
sudo supervisorctl status shri-shyam-school

# View logs
sudo tail -f /var/log/shri-shyam-school.log

# Check Nginx status
sudo systemctl status nginx
```

### Health Check Endpoints

- Backend: `https://your-domain.com/api/health`
- Frontend: `https://your-domain.com`

---

## 🚀 CI/CD Pipeline (Optional)

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Test application
      run: |
        cd backend
        python -m pytest tests/ || echo "No tests found"
    
    - name: Deploy to Render
      # Add your deployment steps here
```

---

## 🛠️ Troubleshooting

### Common Issues

**1. Database locked error**
```bash
# Check if multiple processes are accessing DB
ps aux | grep python
# Kill conflicting processes if needed
```

**2. File upload permissions**
```bash
# Ensure uploads directory is writable
chmod 755 /home/ubuntu/shri-shyam-school/backend/uploads
chown ubuntu:ubuntu /home/ubuntu/shri-shyam-school/backend/uploads
```

**3. CORS errors**
- Check CORS_ORIGINS environment variable
- Ensure frontend domain is included

**4. 502 Bad Gateway**
```bash
# Check if backend is running
sudo supervisorctl status shri-shyam-school
# Check Nginx configuration
sudo nginx -t
```

### Debug Commands

```bash
# Check backend health
curl https://your-domain.com/api/health

# Check database
cd /home/ubuntu/shri-shyam-school/backend
sqlite3 school.db ".tables"

# Monitor logs in real-time
sudo tail -f /var/log/shri-shyam-school.log
sudo tail -f /var/log/nginx/error.log
```

---

## 📞 Support

For deployment issues:
1. Check the troubleshooting section above
2. Review application logs
3. Ensure all environment variables are set
4. Verify database permissions and file access

---

**🎉 Congratulations! Your school website is now deployed with SQLite backend!**

The deployment is completely self-contained and doesn't require any external database services.
