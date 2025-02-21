import os
from app import create_app, db
from app.models import User, Content

app = create_app()

def init_db():
    # Ensure instance directory exists
    os.makedirs('instance', exist_ok=True)
    
    with app.app_context():
        print("Initializing database...")
        try:
            # Create tables if they don't exist
            db.create_all()
            
            # Create default admin user if not exists
            if not User.query.filter_by(username='admin').first():
                print("Creating admin user...")
                admin = User(username='admin')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully")
            
            # Create sample content if not exists
        
            if not Content.query.first():
                print("Creating sample content...")
                sample_content = Content(
                    title='Welcome to My Website',
                    body='This is a sample content. You can edit this through the admin panel.',
                    page='home',
                    image_url=None,
                    external_link=None
                )
                db.session.add(sample_content)
                db.session.commit()
                print("Sample content created successfully")
            
            print("Database initialization completed successfully")
            
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('instance', exist_ok=True)
    os.makedirs(os.path.join('app', 'static', 'uploads'), exist_ok=True)
    
    # Initialize database
    init_db()
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5001)
