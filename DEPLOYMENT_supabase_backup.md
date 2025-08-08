# Deployment Guide - Shri Shyam Public School Website

This guide will help you deploy the school website to production using various hosting platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- ✅ Supabase project set up with database schema
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
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_KEY=your-supabase-service-key
   PORT=10000
   ```

5. **Advanced Settings**
   - Root Directory: `backend`
   - Python Version: 3.11
   - Auto-Deploy: Yes

6. **Deploy**
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
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-supabase-anon-key
   SUPABASE_SERVICE_KEY=your-supabase-service-key
   PORT=8080
   ```

4. **Configure Build**
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
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
sudo apt install python3 python3-pip nginx postgresql postgresql-contrib supervisor git -y

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
# Start supervisor
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
    
    # Backend API
    location /api {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/shri-shyam-school /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Step 5: SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

---

## 🔧 Post-Deployment Configuration

### 1. Update API URLs

After backend deployment, update frontend configuration:

```javascript
// In frontend/js/app.js
const API_BASE_URL = 'https://your-backend-domain.com/api';
const SUPABASE_URL = 'your-supabase-url';
const SUPABASE_ANON_KEY = 'your-supabase-anon-key';
```

### 2. Configure CORS

Update backend CORS origins:

```python
# In backend/app.py
CORS(app, origins=[
    "https://your-frontend-domain.com",
    "https://www.your-frontend-domain.com"
])
```

### 3. Supabase Configuration

Update Supabase settings:
- Go to Settings → API → URL Configuration
- Add your production domains to allowed origins
- Update authentication settings

### 4. DNS Configuration

For custom domain:
```
Type    Name    Content
A       @       your-server-ip
A       www     your-server-ip
```

For Netlify/Vercel:
```
CNAME   @       your-app.netlify.app
CNAME   www     your-app.netlify.app
```

---

## 📊 Performance Optimization

### Frontend Optimizations

1. **Image Optimization**
   ```bash
   # Compress images (optional)
   npm install -g imagemin-cli
   imagemin frontend/images/* --out-dir=frontend/images/optimized
   ```

2. **CSS Minification**
   ```bash
   # Install CSS minifier
   npm install -g clean-css-cli
   cleancss -o frontend/css/styles.min.css frontend/css/styles.css
   ```

3. **JavaScript Minification**
   ```bash
   # Install JS minifier
   npm install -g uglify-js
   uglifyjs frontend/js/app.js -o frontend/js/app.min.js
   ```

### Backend Optimizations

1. **Production Settings**
   ```python
   # In app.py
   if os.environ.get('FLASK_ENV') == 'production':
       app.config['DEBUG'] = False
       app.config['TESTING'] = False
   ```

2. **Database Connection Pooling**
   ```python
   # Add to requirements.txt
   psycopg2-pool==1.1
   ```

---

## 🔍 Monitoring & Maintenance

### 1. Health Monitoring

Set up monitoring for:
- Website uptime
- API response times
- Database performance
- Error rates

Recommended tools:
- **UptimeRobot** (free uptime monitoring)
- **Google Analytics** (website analytics)
- **Sentry** (error tracking)

### 2. Backup Strategy

```bash
# Database backup (if using PostgreSQL)
pg_dump your_database > backup_$(date +%Y%m%d).sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump your_database > /backups/backup_$DATE.sql
find /backups -name "backup_*.sql" -mtime +30 -delete
```

### 3. Log Management

```bash
# View logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/shri-shyam-school.log

# Log rotation
sudo nano /etc/logrotate.d/shri-shyam-school
```

---

## 🚨 Troubleshooting

### Common Issues

**1. 502 Bad Gateway**
```bash
# Check backend service
sudo supervisorctl status shri-shyam-school
sudo supervisorctl restart shri-shyam-school

# Check logs
sudo tail -f /var/log/shri-shyam-school.log
```

**2. Database Connection Issues**
```bash
# Check Supabase connection
curl -I https://your-project.supabase.co

# Test database query
psql -h your-db-host -U your-user -d your-database -c "SELECT version();"
```

**3. CORS Errors**
- Update CORS origins in backend
- Check Supabase allowed origins
- Verify frontend API URLs

**4. SSL Certificate Issues**
```bash
# Renew SSL certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

### Performance Issues

**1. Slow Loading**
- Enable Gzip compression
- Optimize images
- Use CDN for static files
- Database query optimization

**2. High Memory Usage**
- Monitor backend processes
- Implement connection pooling
- Optimize database queries

---

## 📈 Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**
   - Use Nginx or cloud load balancer
   - Multiple backend instances
   - Session management

2. **Database Scaling**
   - Read replicas
   - Connection pooling
   - Query optimization

3. **CDN Integration**
   - CloudFlare or AWS CloudFront
   - Static asset delivery
   - Image optimization

### Vertical Scaling

1. **Server Resources**
   - Increase RAM/CPU
   - SSD storage
   - Better network bandwidth

2. **Database Performance**
   - Proper indexing
   - Query optimization
   - Connection limits

---

## 🔒 Security Checklist

- [ ] HTTPS enabled
- [ ] Strong passwords
- [ ] Regular backups
- [ ] Updated dependencies
- [ ] Firewall configured
- [ ] Rate limiting enabled
- [ ] Input validation
- [ ] SQL injection protection
- [ ] XSS protection
- [ ] CSRF protection

---

## 📞 Support

If you encounter issues during deployment:

1. Check the logs first
2. Review environment variables
3. Verify Supabase configuration
4. Test API endpoints
5. Check DNS/domain settings

For additional support, create an issue on the repository with:
- Deployment method used
- Error messages
- Environment details
- Steps to reproduce

---

**Happy Deploying! 🚀**
