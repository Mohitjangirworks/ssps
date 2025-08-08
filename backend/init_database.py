#!/usr/bin/env python3
"""
Database initialization script for Shri Shyam Public School
This script creates the database tables and adds sample data
"""

import os
import sys
from datetime import datetime, date
import sqlite3

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Admin, News, Event, Result, Topper, Faculty

def init_database():
    """Initialize the database with tables and sample data"""
    
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        
        # Create admin user if doesn't exist
        if not Admin.query.filter_by(username='admin').first():
            admin = Admin(
                username='admin',
                email='admin@shrishyamschool.edu',
                full_name='System Administrator'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("✓ Created admin user: admin/admin123")
        
        # Add sample news
        sample_news = [
            {
                'title': 'Class XII Results Declared - 98% Pass Rate!',
                'content': 'We are proud to announce that our Class XII students have achieved a remarkable 98% pass rate with 15 students securing above 95% marks.',
                'emoji': '🏆',
                'priority': 'high'
            },
            {
                'title': 'State Science Exhibition Winners',
                'content': 'Our students have won first prize in the State Level Science Exhibition for their innovative project on renewable energy.',
                'emoji': '🥇',
                'priority': 'normal'
            },
            {
                'title': 'Admissions Open for 2024-25',
                'content': 'Admissions are now open for the academic year 2024-25. Apply online or visit our campus for more details.',
                'emoji': '🎓',
                'priority': 'normal'
            },
            {
                'title': 'New Science Labs Inaugurated',
                'content': 'State-of-the-art science laboratories with modern equipment have been inaugurated to enhance practical learning.',
                'emoji': '🔬',
                'priority': 'normal'
            }
        ]
        
        for news_data in sample_news:
            if not News.query.filter_by(title=news_data['title']).first():
                news = News(**news_data)
                db.session.add(news)
        
        print("✓ Added sample news items")
        
        # Add sample events
        sample_events = [
            {
                'title': 'Annual Sports Day',
                'description': 'Inter-house sports competitions, athletics, and cultural performances',
                'event_date': date(2024, 12, 15),
                'event_time': '9:00 AM - 4:00 PM',
                'location': 'School Playground',
                'category': 'sports',
                'is_featured': True
            },
            {
                'title': 'Science Exhibition',
                'description': 'Student projects, experiments, and innovative solutions showcase',
                'event_date': date(2024, 12, 20),
                'event_time': '10:00 AM - 2:00 PM',
                'location': 'Science Labs',
                'category': 'academic'
            },
            {
                'title': 'Christmas Celebration',
                'description': 'Carol singing, dance performances, and festive activities',
                'event_date': date(2024, 12, 25),
                'event_time': '11:00 AM - 1:00 PM',
                'location': 'School Auditorium',
                'category': 'cultural'
            },
            {
                'title': 'Republic Day Celebration',
                'description': 'Flag hoisting ceremony, cultural programs, and patriotic performances',
                'event_date': date(2025, 1, 26),
                'event_time': '8:00 AM - 12:00 PM',
                'location': 'School Ground',
                'category': 'cultural',
                'is_featured': True
            }
        ]
        
        for event_data in sample_events:
            if not Event.query.filter_by(title=event_data['title']).first():
                event = Event(**event_data)
                db.session.add(event)
        
        print("✓ Added sample events")
        
        # Add sample results
        sample_results = [
            # Class XII Results
            {
                'class_level': '12',
                'year': 2024,
                'pass_rate': '98%',
                'above_90': 45,
                'above_95': 15,
                'district_rank': '2nd',
                'state_rank': '15th'
            },
            {
                'class_level': '12',
                'year': 2023,
                'pass_rate': '96%',
                'above_90': 38,
                'above_95': 12,
                'district_rank': '3rd',
                'state_rank': '18th'
            },
            {
                'class_level': '12',
                'year': 2022,
                'pass_rate': '94%',
                'above_90': 35,
                'above_95': 10,
                'district_rank': '4th',
                'state_rank': '22nd'
            },
            # Class X Results
            {
                'class_level': '10',
                'year': 2024,
                'pass_rate': '100%',
                'above_90': 52,
                'above_95': 18,
                'district_rank': '1st',
                'state_rank': '8th'
            },
            {
                'class_level': '10',
                'year': 2023,
                'pass_rate': '98%',
                'above_90': 48,
                'above_95': 15,
                'district_rank': '2nd',
                'state_rank': '12th'
            },
            {
                'class_level': '10',
                'year': 2022,
                'pass_rate': '96%',
                'above_90': 42,
                'above_95': 13,
                'district_rank': '3rd',
                'state_rank': '16th'
            }
        ]
        
        for result_data in sample_results:
            if not Result.query.filter_by(
                class_level=result_data['class_level'],
                year=result_data['year']
            ).first():
                result = Result(**result_data)
                db.session.add(result)
        
        print("✓ Added sample results")
        
        # Add sample toppers
        sample_toppers = [
            {
                'name': 'Priya Sharma',
                'class_level': '12',
                'year': 2024,
                'percentage': 98.2,
                'stream': 'Science',
                'achievement': 'District Topper'
            },
            {
                'name': 'Rahul Kumar',
                'class_level': '12',
                'year': 2024,
                'percentage': 97.8,
                'stream': 'Commerce',
                'achievement': 'Stream Topper'
            },
            {
                'name': 'Anita Singh',
                'class_level': '12',
                'year': 2024,
                'percentage': 96.5,
                'stream': 'Arts',
                'achievement': 'Stream Topper'
            },
            {
                'name': 'Vikash Patel',
                'class_level': '10',
                'year': 2024,
                'percentage': 99.2,
                'stream': 'General',
                'achievement': 'District Topper'
            },
            {
                'name': 'Kavya Gupta',
                'class_level': '10',
                'year': 2024,
                'percentage': 98.6,
                'stream': 'General',
                'achievement': 'School Topper'
            }
        ]
        
        for topper_data in sample_toppers:
            if not Topper.query.filter_by(
                name=topper_data['name'],
                year=topper_data['year']
            ).first():
                topper = Topper(**topper_data)
                db.session.add(topper)
        
        print("✓ Added sample toppers")
        
        # Add sample faculty
        sample_faculty = [
            {
                'name': 'Mrs. Sunita Sharma',
                'position': 'Principal',
                'qualifications': 'M.Ed, B.Ed, M.A. (English)',
                'experience': '25+ Years Experience',
                'subjects': 'Educational Leadership, Administration',
                'description': 'Educational leadership and administration specialist with extensive experience in curriculum development.',
                'position_order': 1
            },
            {
                'name': 'Mr. Rajesh Kumar',
                'position': 'Vice Principal',
                'qualifications': 'M.Sc. (Mathematics), B.Ed',
                'experience': '20+ Years Experience',
                'subjects': 'Mathematics, Statistics',
                'description': 'Mathematics department head with expertise in advanced mathematics and analytical thinking.',
                'position_order': 2
            },
            {
                'name': 'Dr. Priya Singh',
                'position': 'Science Department Head',
                'qualifications': 'Ph.D. (Chemistry), M.Sc., B.Ed',
                'experience': '15+ Years Experience',
                'subjects': 'Chemistry, Physics',
                'description': 'Research-oriented chemistry teacher focusing on practical applications and scientific methodology.',
                'position_order': 3
            },
            {
                'name': 'Mrs. Meera Gupta',
                'position': 'English Teacher',
                'qualifications': 'M.A. (English), B.Ed',
                'experience': '18+ Years Experience',
                'subjects': 'English Literature, Communication',
                'description': 'Language specialist with focus on communication skills and literature appreciation.',
                'position_order': 4
            },
            {
                'name': 'Mr. Amit Verma',
                'position': 'Computer Science Teacher',
                'qualifications': 'MCA, B.Tech (IT)',
                'experience': '12+ Years Experience',
                'subjects': 'Computer Science, Programming',
                'description': 'Technology educator specializing in programming, web development, and digital literacy.',
                'position_order': 5
            },
            {
                'name': 'Mrs. Sushila Yadav',
                'position': 'Hindi Teacher',
                'qualifications': 'M.A. (Hindi), B.Ed',
                'experience': '16+ Years Experience',
                'subjects': 'Hindi Literature, Grammar',
                'description': 'Hindi language and literature expert with focus on cultural values and communication skills.',
                'position_order': 6
            }
        ]
        
        for faculty_data in sample_faculty:
            if not Faculty.query.filter_by(name=faculty_data['name']).first():
                faculty = Faculty(**faculty_data)
                db.session.add(faculty)
        
        print("✓ Added sample faculty")
        
        # Commit all changes
        try:
            db.session.commit()
            print("✅ Database initialization completed successfully!")
            print("\nDatabase file created at: school.db")
            print("\nAdmin login credentials:")
            print("Username: admin")
            print("Password: admin123")
            print("\nYou can now start the Flask application:")
            print("python app_sqlite.py")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error during database initialization: {e}")
            raise

def reset_database():
    """Reset the database by dropping all tables and recreating them"""
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("✓ All tables dropped")
        
        init_database()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()
