import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client, Client
from datetime import datetime, timedelta
import jwt
from functools import wraps
import uuid
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SUPABASE_URL'] = os.environ.get('SUPABASE_URL', 'YOUR_SUPABASE_URL')
app.config['SUPABASE_KEY'] = os.environ.get('SUPABASE_KEY', 'YOUR_SUPABASE_ANON_KEY')
app.config['SUPABASE_SERVICE_KEY'] = os.environ.get('SUPABASE_SERVICE_KEY', 'YOUR_SUPABASE_SERVICE_KEY')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS
CORS(app, origins=[
    "http://localhost:3000", 
    "http://localhost:8080", 
    "http://127.0.0.1:5500",
    "https://your-domain.com"  # Add your production domain
])

# Initialize Supabase client
supabase: Client = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            if token.startswith('Bearer '):
                token = token.split(' ')[1]
            
            # Verify token with Supabase
            user = supabase.auth.get_user(token)
            if not user:
                return jsonify({'error': 'Token is invalid'}), 401
                
        except Exception as e:
            return jsonify({'error': 'Token is invalid'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

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

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'Shri Shyam Public School API'
    })

# News and Announcements
@app.route('/api/news', methods=['GET'])
def get_news():
    """Get latest news and announcements"""
    try:
        result = supabase.table('news').select('*').order('created_at', desc=True).limit(10).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/news', methods=['POST'])
@token_required
def create_news():
    """Create new news item (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'content']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        # Sanitize input
        news_data = {
            'id': str(uuid.uuid4()),
            'title': sanitize_input(data['title']),
            'content': sanitize_input(data['content']),
            'emoji': data.get('emoji', '📢'),
            'priority': data.get('priority', 'normal'),
            'is_active': data.get('is_active', True),
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('news').insert(news_data).execute()
        return jsonify(result.data[0]), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Admissions
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
        
        # Sanitize and prepare data
        admission_data = {
            'id': str(uuid.uuid4()),
            'student_name': sanitize_input(data['studentName']),
            'class_applying': sanitize_input(data['classApplying']),
            'date_of_birth': data['dateOfBirth'],
            'gender': sanitize_input(data['gender']),
            'father_name': sanitize_input(data['fatherName']),
            'mother_name': sanitize_input(data['motherName']),
            'phone': sanitize_input(data['phone']),
            'email': sanitize_input(data['email']),
            'address': sanitize_input(data['address']),
            'previous_school': sanitize_input(data.get('previousSchool', '')),
            'previous_percentage': data.get('previousPercentage'),
            'application_status': 'pending',
            'submitted_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('admissions').insert(admission_data).execute()
        
        # Send confirmation email (you can implement this)
        # send_admission_confirmation_email(admission_data)
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': result.data[0]['id']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admissions', methods=['GET'])
@token_required
def get_admissions():
    """Get all admission applications (Admin only)"""
    try:
        # Get query parameters
        status = request.args.get('status', 'all')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit
        
        # Build query
        query = supabase.table('admissions').select('*')
        
        if status != 'all':
            query = query.eq('application_status', status)
        
        result = query.order('submitted_at', desc=True).range(offset, offset + limit - 1).execute()
        
        # Get total count
        count_result = supabase.table('admissions').select('id', count='exact')
        if status != 'all':
            count_result = count_result.eq('application_status', status)
        count_data = count_result.execute()
        
        return jsonify({
            'admissions': result.data,
            'total': count_data.count,
            'page': page,
            'limit': limit,
            'total_pages': (count_data.count + limit - 1) // limit
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/admissions/<admission_id>/status', methods=['PUT'])
@token_required
def update_admission_status(admission_id):
    """Update admission application status (Admin only)"""
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if new_status not in ['pending', 'approved', 'rejected', 'waitlisted']:
            return jsonify({'error': 'Invalid status'}), 400
        
        result = supabase.table('admissions').update({
            'application_status': new_status,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', admission_id).execute()
        
        if not result.data:
            return jsonify({'error': 'Application not found'}), 404
        
        return jsonify({'message': 'Status updated successfully'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Contact Messages
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
        
        # Sanitize and prepare data
        contact_data = {
            'id': str(uuid.uuid4()),
            'name': sanitize_input(data['name']),
            'email': sanitize_input(data['email']),
            'phone': sanitize_input(data.get('phone', '')),
            'subject': sanitize_input(data['subject']),
            'message': sanitize_input(data['message']),
            'status': 'unread',
            'submitted_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('contact_messages').insert(contact_data).execute()
        
        return jsonify({'message': 'Message sent successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/contact', methods=['GET'])
@token_required
def get_contact_messages():
    """Get all contact messages (Admin only)"""
    try:
        status = request.args.get('status', 'all')
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 20))
        offset = (page - 1) * limit
        
        query = supabase.table('contact_messages').select('*')
        
        if status != 'all':
            query = query.eq('status', status)
        
        result = query.order('submitted_at', desc=True).range(offset, offset + limit - 1).execute()
        
        # Get total count
        count_result = supabase.table('contact_messages').select('id', count='exact')
        if status != 'all':
            count_result = count_result.eq('status', status)
        count_data = count_result.execute()
        
        return jsonify({
            'messages': result.data,
            'total': count_data.count,
            'page': page,
            'limit': limit,
            'total_pages': (count_data.count + limit - 1) // limit
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Events
@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    try:
        result = supabase.table('events').select('*').order('event_date', desc=False).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events', methods=['POST'])
@token_required
def create_event():
    """Create new event (Admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'event_date', 'location']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        event_data = {
            'id': str(uuid.uuid4()),
            'title': sanitize_input(data['title']),
            'description': sanitize_input(data['description']),
            'event_date': data['event_date'],
            'event_time': data.get('event_time', ''),
            'location': sanitize_input(data['location']),
            'category': sanitize_input(data.get('category', 'general')),
            'is_featured': data.get('is_featured', False),
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('events').insert(event_data).execute()
        return jsonify(result.data[0]), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Results
@app.route('/api/results', methods=['GET'])
def get_results():
    """Get academic results data"""
    try:
        # Get Class X results
        class10_result = supabase.table('results').select('*').eq('class_level', '10').order('year', desc=True).execute()
        
        # Get Class XII results
        class12_result = supabase.table('results').select('*').eq('class_level', '12').order('year', desc=True).execute()
        
        # Get toppers
        toppers_result = supabase.table('toppers').select('*').order('year', desc=True).limit(10).execute()
        
        return jsonify({
            'class10': class10_result.data,
            'class12': class12_result.data,
            'toppers': toppers_result.data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results', methods=['POST'])
@token_required
def create_result():
    """Create new result entry (Admin only)"""
    try:
        data = request.get_json()
        
        required_fields = ['class_level', 'year', 'pass_rate']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        result_data = {
            'id': str(uuid.uuid4()),
            'class_level': data['class_level'],
            'year': data['year'],
            'pass_rate': data['pass_rate'],
            'above_90': data.get('above_90', 0),
            'above_95': data.get('above_95', 0),
            'district_rank': data.get('district_rank', ''),
            'state_rank': data.get('state_rank', ''),
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('results').insert(result_data).execute()
        return jsonify(result.data[0]), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Gallery
@app.route('/api/gallery', methods=['GET'])
def get_gallery():
    """Get gallery images"""
    try:
        result = supabase.table('gallery').select('*').eq('is_active', True).order('created_at', desc=True).execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/gallery', methods=['POST'])
@token_required
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
        
        # Upload to Supabase Storage
        file_content = file.read()
        storage_result = supabase.storage.from_('gallery').upload(filename, file_content)
        
        if hasattr(storage_result, 'error') and storage_result.error:
            return jsonify({'error': 'Failed to upload image'}), 500
        
        # Get public URL
        public_url = supabase.storage.from_('gallery').get_public_url(filename)
        
        # Save to database
        gallery_data = {
            'id': str(uuid.uuid4()),
            'title': request.form.get('title', 'Untitled'),
            'description': request.form.get('description', ''),
            'image_url': public_url,
            'category': request.form.get('category', 'general'),
            'is_active': True,
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('gallery').insert(gallery_data).execute()
        return jsonify(result.data[0]), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Faculty
@app.route('/api/faculty', methods=['GET'])
def get_faculty():
    """Get faculty members"""
    try:
        result = supabase.table('faculty').select('*').eq('is_active', True).order('position_order').execute()
        return jsonify(result.data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/faculty', methods=['POST'])
@token_required
def create_faculty():
    """Create faculty member (Admin only)"""
    try:
        data = request.get_json()
        
        required_fields = ['name', 'position', 'qualifications']
        is_valid, error_message = validate_required_fields(data, required_fields)
        if not is_valid:
            return jsonify({'error': error_message}), 400
        
        faculty_data = {
            'id': str(uuid.uuid4()),
            'name': sanitize_input(data['name']),
            'position': sanitize_input(data['position']),
            'qualifications': sanitize_input(data['qualifications']),
            'experience': sanitize_input(data.get('experience', '')),
            'subjects': data.get('subjects', []),
            'description': sanitize_input(data.get('description', '')),
            'photo_url': data.get('photo_url', ''),
            'position_order': data.get('position_order', 0),
            'is_active': True,
            'created_at': datetime.utcnow().isoformat()
        }
        
        result = supabase.table('faculty').insert(faculty_data).execute()
        return jsonify(result.data[0]), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Statistics Dashboard
@app.route('/api/dashboard/stats', methods=['GET'])
@token_required
def get_dashboard_stats():
    """Get dashboard statistics (Admin only)"""
    try:
        # Count admissions by status
        pending_admissions = supabase.table('admissions').select('id', count='exact').eq('application_status', 'pending').execute()
        total_admissions = supabase.table('admissions').select('id', count='exact').execute()
        
        # Count unread messages
        unread_messages = supabase.table('contact_messages').select('id', count='exact').eq('status', 'unread').execute()
        
        # Count active events
        today = datetime.utcnow().date().isoformat()
        upcoming_events = supabase.table('events').select('id', count='exact').gte('event_date', today).execute()
        
        # Count active faculty
        active_faculty = supabase.table('faculty').select('id', count='exact').eq('is_active', True).execute()
        
        return jsonify({
            'admissions': {
                'total': total_admissions.count,
                'pending': pending_admissions.count
            },
            'messages': {
                'unread': unread_messages.count
            },
            'events': {
                'upcoming': upcoming_events.count
            },
            'faculty': {
                'active': active_faculty.count
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

# Development server
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)
