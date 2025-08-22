# LORD'S HEART EDUCATIONAL COMPLEX - School Management System

A comprehensive Django REST API backend for managing school admissions, contact forms, and user management.

## Features

### Admissions Management
- **Complete Application Tracking**: Store and manage pupil admission applications with comprehensive data fields
- **Status Management**: Track applications through pending, reviewed, accepted, and rejected statuses
- **Parent/Guardian Information**: Store detailed contact and personal information
- **Validation**: Comprehensive input validation and data integrity checks
- **Admin Dashboard**: Rich admin interface with filtering, searching, and bulk actions

### Contact Management
- **Visitor Contact Forms**: Public contact form submission with automatic data capture
- **Message Status Tracking**: New, read, replied, and archived status management
- **IP and User Agent Tracking**: Automatic capture of visitor information
- **Admin Interface**: Complete message management with email integration

### User Management
- **Role-Based Access Control**: Admin, staff, teacher, parent, and student roles
- **Extended User Profiles**: Additional user information and professional details
- **Secure Authentication**: Django's built-in authentication with custom permissions
- **Profile Management**: User profile updates and password changes

### API Features
- **RESTful Design**: Complete REST API with proper HTTP methods
- **Role-Based Permissions**: Secure access control based on user roles
- **Filtering and Search**: Advanced filtering, searching, and ordering capabilities
- **Pagination**: Efficient data pagination for large datasets
- **Statistics Endpoints**: Dashboard statistics and analytics

## Technology Stack

- **Backend**: Django 4.2.7 + Django REST Framework 3.14.0
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: Django's built-in authentication system
- **API Documentation**: Auto-generated with DRF
- **Testing**: Comprehensive unit tests with Django TestCase
- **Deployment**: Heroku-ready with Gunicorn

## Installation and Setup

### Prerequisites
- Python 3.11+
- pip
- virtualenv (recommended)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd school-management-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

5. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

### Production Deployment

1. **Set up production environment variables**
   ```bash
   # Update .env with production settings
   DEBUG=False
   SECRET_KEY=your-production-secret-key
   DATABASE_URL=postgresql://user:password@host:port/dbname
   ```

2. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

3. **Deploy to your preferred platform**
   - **Heroku**: Push to Heroku Git repository
   - **AWS**: Use Elastic Beanstalk or EC2
   - **DigitalOcean**: Deploy to App Platform or Droplet

## API Endpoints

### Admissions API
- `GET /api/admissions/` - List applications (public read, admin full access)
- `POST /api/admissions/` - Create new application (public)
- `GET /api/admissions/{id}/` - Get application details (admin only)
- `PUT /api/admissions/{id}/` - Update application (admin only)
- `DELETE /api/admissions/{id}/` - Delete application (admin only)
- `GET /api/admissions/statistics/` - Get admission statistics (admin only)
- `GET /api/admissions/pending/` - Get pending applications (admin only)
- `POST /api/admissions/{id}/approve/` - Approve application (admin only)
- `POST /api/admissions/{id}/reject/` - Reject application (admin only)

### Contact API
- `GET /api/contact/` - List messages (admin only)
- `POST /api/contact/` - Create new message (public)
- `GET /api/contact/{id}/` - Get message details (admin only)
- `PUT /api/contact/{id}/` - Update message (admin only)
- `DELETE /api/contact/{id}/` - Delete message (admin only)
- `GET /api/contact/statistics/` - Get contact statistics (admin only)
- `GET /api/contact/new/` - Get new messages (admin only)
- `POST /api/contact/{id}/mark_as_read/` - Mark as read (admin only)
- `POST /api/contact/{id}/mark_as_replied/` - Mark as replied (admin only)
- `POST /api/contact/{id}/archive/` - Archive message (admin only)

### Users API
- `GET /api/users/` - List users (admin only)
- `POST /api/users/` - Create new user (admin only)
- `GET /api/users/{id}/` - Get user details (admin only)
- `PUT /api/users/{id}/` - Update user (admin only)
- `DELETE /api/users/{id}/` - Delete user (admin only)
- `GET /api/users/me/` - Get current user profile
- `PUT /api/users/update_me/` - Update current user profile
- `POST /api/users/change_password/` - Change password
- `GET /api/users/statistics/` - Get user statistics (admin only)

## Database Schema

### AdmissionApplication
- **Pupil Data**: surname, first_name, other_names, date_of_birth, age, gender, etc.
- **Parent Data**: father_name, mother_name, contacts, emails, addresses
- **Application Status**: pending, reviewed, accepted, rejected
- **Metadata**: application_date, reviewed_date, reviewed_by, notes

### ContactMessage
- **Contact Info**: name, email, message
- **Status**: new, read, replied, archived
- **Metadata**: ip_address, user_agent, timestamps

### UserProfile
- **User Info**: role, phone_number, address, date_of_birth
- **Professional Info**: department, employee_id
- **Extended Data**: profile_picture, additional fields

## Testing

Run the test suite:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test admissions
python manage.py test contact
python manage.py test users
```

## Admin Interface

Access the Django admin interface at `/admin/` after creating a superuser. The admin interface provides:

- **Admissions Management**: Complete application tracking with bulk actions
- **Contact Management**: Message status management and email integration
- **User Management**: User and profile management with role assignments
- **Statistics**: Dashboard with key metrics and analytics

## Security Features

- **Input Validation**: Comprehensive validation for all form inputs
- **Role-Based Permissions**: Secure access control based on user roles
- **CSRF Protection**: Built-in CSRF protection for all forms
- **SQL Injection Protection**: Django ORM protection against SQL injection
- **XSS Protection**: Automatic XSS protection in templates and forms
- **Secure Headers**: Security headers for production deployment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact the development team or create an issue in the repository.

## Changelog

### Version 1.0.0
- Initial release
- Complete admissions management system
- Contact form management
- User management with role-based access
- Comprehensive API endpoints
- Admin interface
- Unit tests
- Production deployment configuration
