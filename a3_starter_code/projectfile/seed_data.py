from website import create_app, db
from website.models import User, Event, Comment, Order
from flask_bcrypt import generate_password_hash
from datetime import datetime, timedelta

def seed_data():
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        admin_user = User( # Admin user for the application
            first_name='Admin',
            surname='User',
            name='admin',
            email='admin@example.com',
            contact_number='0412345678',
            street_address='123 Admin Street, Brisbane QLD 4000',
            password_hash=generate_password_hash('password').decode('utf-8')
        )
        
        test_user = User( # Regular test user
            first_name='John',
            surname='Doe',
            name='johndoe',
            email='john@example.com',
            contact_number='0423456789',
            street_address='456 Test Avenue, Brisbane QLD 4001',
            password_hash=generate_password_hash('password').decode('utf-8')
        )
        
        db.session.add(admin_user)
        db.session.add(test_user)
        db.session.commit()
        
        events_data = [ # Sample events to seed the database
            {
                'name': 'Jazz Night Live',
                'description': 'Join us at the Brisbane Jazz Club in Kangaroo Point for a smooth night of live jazz with riverside views and some of the best local musicians in town.',
                'date': datetime.now() + timedelta(days=30),
                'venue': 'Brisbane Jazz Club, Kangaroo Point',
                'category': 'Jazz',
                'price': 35.00,
                'tickets_available': 50,
                'image': 'jazz-night.jpg',
                'user_id': admin_user.id
            },
            {
                'name': 'Rock Fest 2025',
                'description': 'Set against the city skyline at Riverstage, this open-air rock event features Queensland\'s loudest bands, live food stalls, and a full-scale sound system.',
                'date': datetime.now() + timedelta(days=45),
                'venue': 'Riverstage, Brisbane',
                'category': 'Rock',
                'price': 65.00,
                'tickets_available': 0,
                'image': 'rock-fest.jpg',
                'status': 'Sold Out',
                'user_id': admin_user.id
            },
            {
                'name': 'Baseline Underground',
                'description': 'Deep house and techno takes over The Warehouse Brisbane with local and international DJs bringing energy from 9PM through till late.',
                'date': datetime.now() - timedelta(days=10),
                'venue': 'The Warehouse Brisbane',
                'category': 'Electronic',
                'price': 45.00,
                'tickets_available': 30,
                'image': 'electro-nights.jpg',
                'status': 'Inactive',
                'user_id': admin_user.id
            },
            {
                'name': 'Classical Gala Evening',
                'description': 'Experience a live orchestral performance at the HOTA Outdoor Stage in Bundall, featuring the Gold Coast Philharmonic and open-air seating on the lawn.',
                'date': datetime.now() + timedelta(days=60),
                'venue': 'HOTA Outdoor Stage, Bundall',
                'category': 'Classical',
                'price': 55.00,
                'tickets_available': 100,
                'image': 'classical-gala.jpg',
                'user_id': test_user.id
            },
            {
                'name': 'Hip-Hop Battle Underground',
                'description': 'Raw talent and freestyle heat. Watch MCs clash live in an underground battle.',
                'date': datetime.now() + timedelta(days=20),
                'venue': 'Underground Venue, Brisbane',
                'category': 'Hip-Hop',
                'price': 25.00,
                'tickets_available': 75,
                'image': 'hiphop-battle.jpeg',
                'status': 'Cancelled',
                'user_id': test_user.id
            }
        ]
        
        for event_data in events_data: 
            event = Event(**event_data)
            db.session.add(event)
        
        db.session.commit()
        
        sample_comment = Comment( # Sample comment for an event
            content='This looks amazing! Can\'t wait to attend.',
            user_id=test_user.id,
            event_id=1
        )
        
        db.session.add(sample_comment)
        db.session.commit()
        
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data() 