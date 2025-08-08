import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from datetime import datetime, timedelta
import uuid
from werkzeug.utils import secure_filename
from functools import wraps
import re

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///school.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-string')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Enable CORS
CORS(app, origins=[
    "http://localhost:3000", 
    "http://localhost:8080", 
    "http://127.0.0.1:5500",
    "http://localhost:5000",
    "file://"  # For local file access
])

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database Models
class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

class News(db.Model):
    __tablename__ = 'news'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    emoji = db.Column(db.String(10), default='📢')
    priority = db.Column(db.String(20), default='normal')  # normal, high, urgent
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Admission(db.Model):
    __tablename__ = 'admissions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    student_name = db.Column(db.String(100), nullable=False)
    class_applying = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    mother_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    address = db.Column(db.Text, nullable=False)
    previous_school = db.Column(db.String(200))
    previous_percentage = db.Column(db.Float)
    application_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected, waitlisted
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    admin_notes = db.Column(db.Text)

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='unread')  # unread, read, replied
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    replied_at = db.Column(db.DateTime)
    admin_reply = db.Column(db.Text)

class Event(db.Model):
    __tablename__ = 'events'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_time = db.Column(db.String(20))
    location = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='general')  # academic, sports, cultural, general
    is_featured = db.Column(db.Boolean, default=False)
    image_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Result(db.Model):
    __tablename__ = 'results'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    class_level = db.Column(db.String(10), nullable=False)  # 10, 12
    year = db.Column(db.Integer, nullable=False)
    pass_rate = db.Column(db.String(10), nullable=False)
    above_90 = db.Column(db.Integer, default=0)
    above_95 = db.Column(db.Integer, default=0)
    district_rank = db.Column(db.String(20))
    state_rank = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Topper(db.Model):
    __tablename__ = 'toppers'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    class_level = db.Column(db.String(10), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    stream = db.Column(db.String(50), nullable=False)  # Science, Commerce, Arts
    achievement = db.Column(db.String(200))  # District Topper, State Topper, etc.
    photo_url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Gallery(db.Model):
    __tablename__ = 'gallery'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), default='general')  # events, facilities, sports, academic
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Faculty(db.Model):
    __tablename__ = 'faculty'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.String(200), nullable=False)
    experience = db.Column(db.String(100))
    subjects = db.Column(db.Text)  # JSON string of subjects
    description = db.Column(db.Text)
    photo_url = db.Column(db.String(500))
    position_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Helper functions
def validate_required_fields(data, required_fields):
    """Validate that all required fields are present in data"""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    return True, None

def sanitize_input(text):
    """Basic input sanitization"""
    if isinstance(text, str):
        return text.strip()
    return text

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\+]?[0-9\s\-\(\)]{10,}$'
    return re.match(pattern, phone) is not None

# Authentication decorator for admin routes
def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()
        admin = Admin.query.get(current_user_id)
        if not admin or not admin.is_active:
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()
    
    # Create default admin user if doesn't exist
    if not Admin.query.filter_by(username='admin').first():
        admin = Admin(
            username='admin',
            email='admin@shrishyamschool.edu',
            full_name='System Administrator'
        )
        admin.set_password('admin123')  # Change this in production
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created: admin/admin123")

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Shri Shyam Public School API',
        'database': 'SQLite'
    })

# Authentication Routes
@app.route('/api/auth/login', methods=['POST'])
def login():
    """Admin login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password required'}), 400
        
        admin = Admin.query.filter_by(username=data['username']).first()
        
        if admin and admin.check_password(data['password']) and admin.is_active:
            admin.last_login = datetime.utcnow()
            db.session.commit()
            
            access_token = create_access_token(identity=admin.id)
            return jsonify({
                'access_token': access_token,
                'admin': {
                    'id': admin.id,
                    'username': admin.username,
                    'full_name': admin.full_name,
                    'email': admin.email
                }
            })
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current admin user info"""
    try:
        current_user_id = get_jwt_identity()
        admin = Admin.query.get(current_user_id)
        
        if not admin:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': admin.id,
            'username': admin.username,
            'full_name': admin.full_name,
            'email': admin.email,
            'last_login': admin.last_login.isoformat() if admin.last_login else None
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# News Routes
@app.route('/api/news', methods=['GET'])
def get_news():
    """Get latest news and announcements"""
    try:
        news_items = News.query.filter_by(is_active=True).order_by(News.created_at.desc()).limit(10).all()
        
        return jsonify([{
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'emoji': news.emoji,
            'priority': news.priority,
            'created_at': news.created_at.isoformat()
        } for news in news_items])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news', methods=['POST'])
@admin_required
def create_news():
    """Create new news item (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'content']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        news = News(
            title=sanitize_input(data['title']),
            content=sanitize_input(data['content']),
            emoji=data.get('emoji', '📢'),
            priority=data.get('priority', 'normal')
        )
        
        db.session.add(news)
        db.session.commit()
        
        return jsonify({
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'emoji': news.emoji,
            'priority': news.priority,
            'created_at': news.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Admission Routes
@app.route('/api/admissions', methods=['POST'])
def submit_admission():
    """Submit admission application"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = [
            'studentName', 'classApplying', 'dateOfBirth', 'gender',
            'fatherName', 'motherName', 'phone', 'email', 'address'
        ]
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Validate email and phone
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_phone(data['phone']):
            return jsonify({'error': 'Invalid phone number format'}), 400
        
        # Parse date of birth
        try:
            dob = datetime.strptime(data['dateOfBirth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        admission = Admission(
            student_name=sanitize_input(data['studentName']),
            class_applying=sanitize_input(data['classApplying']),
            date_of_birth=dob,
            gender=sanitize_input(data['gender']),
            father_name=sanitize_input(data['fatherName']),
            mother_name=sanitize_input(data['motherName']),
            phone=sanitize_input(data['phone']),
            email=sanitize_input(data['email']),
            address=sanitize_input(data['address']),
            previous_school=sanitize_input(data.get('previousSchool', '')),
            previous_percentage=data.get('previousPercentage')
        )
        
        db.session.add(admission)
        db.session.commit()
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': admission.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/admissions', methods=['GET'])
@admin_required
def get_admissions():
    """Get all admission applications (Admin only)"""
    try:
        status = request.args.get('status', 'all')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        query = Admission.query
        
        if status != 'all':
            query = query.filter_by(application_status=status)
        
        total = query.count()
        admissions = query.order_by(Admission.submitted_at.desc()).offset((page - 1) * limit).limit(limit).all()
        
        return jsonify({
            'admissions': [{
                'id': admission.id,
                'student_name': admission.student_name,
                'class_applying': admission.class_applying,
                'date_of_birth': admission.date_of_birth.isoformat(),
                'gender': admission.gender,
                'father_name': admission.father_name,
                'mother_name': admission.mother_name,
                'phone': admission.phone,
                'email': admission.email,
                'address': admission.address,
                'previous_school': admission.previous_school,
                'previous_percentage': admission.previous_percentage,
                'application_status': admission.application_status,
                'submitted_at': admission.submitted_at.isoformat(),
                'admin_notes': admission.admin_notes
            } for admission in admissions],
            'total': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admissions/<admission_id>/status', methods=['PUT'])
@admin_required
def update_admission_status(admission_id):
    """Update admission application status (Admin only)"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'approved', 'rejected', 'waitlisted']:
            return jsonify({'error': 'Invalid status'}), 400
        
        admission = Admission.query.get_or_404(admission_id)
        admission.application_status = new_status
        admission.admin_notes = data.get('notes', admission.admin_notes)
        admission.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({'message': 'Status updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Contact Routes
@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Submit contact form message"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Validate email
        if not validate_email(data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        contact_message = ContactMessage(
            name=sanitize_input(data['name']),
            email=sanitize_input(data['email']),
            phone=sanitize_input(data.get('phone', '')),
            subject=sanitize_input(data['subject']),
            message=sanitize_input(data['message'])
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        return jsonify({'message': 'Message sent successfully'}), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['GET'])
@admin_required
def get_contact_messages():
    """Get all contact messages (Admin only)"""
    try:
        status = request.args.get('status', 'all')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        
        query = ContactMessage.query
        
        if status != 'all':
            query = query.filter_by(status=status)
        
        total = query.count()
        messages = query.order_by(ContactMessage.submitted_at.desc()).offset((page - 1) * limit).limit(limit).all()
        
        return jsonify({
            'messages': [{
                'id': message.id,
                'name': message.name,
                'email': message.email,
                'phone': message.phone,
                'subject': message.subject,
                'message': message.message,
                'status': message.status,
                'submitted_at': message.submitted_at.isoformat(),
                'replied_at': message.replied_at.isoformat() if message.replied_at else None,
                'admin_reply': message.admin_reply
            } for message in messages],
            'total': total,
            'page': page,
            'limit': limit,
            'total_pages': (total + limit - 1) // limit
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Event Routes
@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    try:
        events = Event.query.order_by(Event.event_date.asc()).all()
        
        return jsonify([{
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.event_date.isoformat(),
            'time': event.event_time,
            'location': event.location,
            'category': event.category,
            'is_featured': event.is_featured,
            'image_url': event.image_url,
            'created_at': event.created_at.isoformat()
        } for event in events])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['POST'])
@admin_required
def create_event():
    """Create new event (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'event_date', 'location']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Parse event date
        try:
            event_date = datetime.strptime(data['event_date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        event = Event(
            title=sanitize_input(data['title']),
            description=sanitize_input(data['description']),
            event_date=event_date,
            event_time=data.get('event_time', ''),
            location=sanitize_input(data['location']),
            category=sanitize_input(data.get('category', 'general')),
            is_featured=data.get('is_featured', False),
            image_url=data.get('image_url', '')
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'date': event.event_date.isoformat(),
            'time': event.event_time,
            'location': event.location,
            'category': event.category,
            'is_featured': event.is_featured,
            'created_at': event.created_at.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Result Routes
@app.route('/api/results', methods=['GET'])
def get_results():
    """Get academic results data"""
    try:
        # Get Class X results
        class10_results = Result.query.filter_by(class_level='10').order_by(Result.year.desc()).all()
        
        # Get Class XII results
        class12_results = Result.query.filter_by(class_level='12').order_by(Result.year.desc()).all()
        
        # Get toppers
        toppers = Topper.query.order_by(Topper.year.desc()).limit(10).all()
        
        return jsonify({
            'class10': [{
                'year': result.year,
                'passRate': result.pass_rate,
                'above90': result.above_90,
                'above95': result.above_95,
                'districtRank': result.district_rank,
                'stateRank': result.state_rank
            } for result in class10_results],
            'class12': [{
                'year': result.year,
                'passRate': result.pass_rate,
                'above90': result.above_90,
                'above95': result.above_95,
                'districtRank': result.district_rank,
                'stateRank': result.state_rank
            } for result in class12_results],
            'toppers': [{
                'name': topper.name,
                'percentage': topper.percentage,
                'stream': topper.stream,
                'achievement': topper.achievement,
                'photo': topper.photo_url,
                'year': topper.year
            } for topper in toppers]
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results', methods=['POST'])
@admin_required
def create_result():
    """Create new result entry (Admin only)"""
    try:
        data = request.get_json()
        
        required_fields = ['class_level', 'year', 'pass_rate']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        result = Result(
            class_level=data['class_level'],
            year=data['year'],
            pass_rate=data['pass_rate'],
            above_90=data.get('above_90', 0),
            above_95=data.get('above_95', 0),
            district_rank=data.get('district_rank', ''),
            state_rank=data.get('state_rank', '')
        )
        
        db.session.add(result)
        db.session.commit()
        
        return jsonify({
            'id': result.id,
            'class_level': result.class_level,
            'year': result.year,
            'pass_rate': result.pass_rate,
            'above_90': result.above_90,
            'above_95': result.above_95,
            'district_rank': result.district_rank,
            'state_rank': result.state_rank
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Gallery Routes
@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Get gallery images"""
    try:
        images = Gallery.query.filter_by(is_active=True).order_by(Gallery.created_at.desc()).all()
        
        return jsonify([{
            'id': image.id,
            'title': image.title,
            'description': image.description,
            'image_url': image.image_url,
            'category': image.category,
            'created_at': image.created_at.isoformat()
        } for image in images])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gallery', methods=['POST'])
@admin_required
def upload_gallery_image():
    """Upload gallery image (Admin only)"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if '.' not in file.filename or file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'error': 'Invalid file type'}), 400
        
        # Generate unique filename
        filename = secure_filename(f"{uuid.uuid4()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(filepath)
        
        # Create gallery entry
        gallery_item = Gallery(
            title=request.form.get('title', 'Untitled'),
            description=request.form.get('description', ''),
            image_url=f'/api/uploads/{filename}',
            category=request.form.get('category', 'general')
        )
        
        db.session.add(gallery_item)
        db.session.commit()
        
        return jsonify({
            'id': gallery_item.id,
            'title': gallery_item.title,
            'description': gallery_item.description,
            'image_url': gallery_item.image_url,
            'category': gallery_item.category
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Faculty Routes
@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    """Get faculty members"""
    try:
        faculty_members = Faculty.query.filter_by(is_active=True).order_by(Faculty.position_order).all()
        
        return jsonify([{
            'id': faculty.id,
            'name': faculty.name,
            'position': faculty.position,
            'qualifications': faculty.qualifications,
            'experience': faculty.experience,
            'subjects': faculty.subjects,
            'description': faculty.description,
            'photo_url': faculty.photo_url,
            'position_order': faculty.position_order
        } for faculty in faculty_members])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faculty', methods=['POST'])
@admin_required
def create_faculty():
    """Create faculty member (Admin only)"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'position', 'qualifications']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        faculty = Faculty(
            name=sanitize_input(data['name']),
            position=sanitize_input(data['position']),
            qualifications=sanitize_input(data['qualifications']),
            experience=sanitize_input(data.get('experience', '')),
            subjects=data.get('subjects', ''),
            description=sanitize_input(data.get('description', '')),
            photo_url=data.get('photo_url', ''),
            position_order=data.get('position_order', 0)
        )
        
        db.session.add(faculty)
        db.session.commit()
        
        return jsonify({
            'id': faculty.id,
            'name': faculty.name,
            'position': faculty.position,
            'qualifications': faculty.qualifications,
            'experience': faculty.experience,
            'subjects': faculty.subjects,
            'description': faculty.description,
            'photo_url': faculty.photo_url,
            'position_order': faculty.position_order
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Dashboard Stats
@app.route('/api/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    """Get dashboard statistics (Admin only)"""
    try:
        # Count admissions by status
        total_admissions = Admission.query.count()
        pending_admissions = Admission.query.filter_by(application_status='pending').count()
        
        # Count unread messages
        unread_messages = ContactMessage.query.filter_by(status='unread').count()
        
        # Count upcoming events
        today = datetime.utcnow().date()
        upcoming_events = Event.query.filter(Event.event_date >= today).count()
        
        # Count active faculty
        active_faculty = Faculty.query.filter_by(is_active=True).count()
        
        return jsonify({
            'admissions': {
                'total': total_admissions,
                'pending': pending_admissions
            },
            'messages': {
                'unread': unread_messages
            },
            'events': {
                'upcoming': upcoming_events
            },
            'faculty': {
                'active': active_faculty
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# File serving route
@app.route('/api/uploads/<filename>')
def serve_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Development server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    with app.app_context():
        db.create_all()
        
        # Create default admin user if doesn't exist
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                email='admin@shrishyamschool.edu',
                full_name='System Administrator'
            )
            admin.set_password('admin123')  # Change this in production
            db.session.add(admin)
            db.session.commit()
            print("Default admin user created: admin/admin123")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
