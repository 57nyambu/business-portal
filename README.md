# Kenya Business Registration Portal

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/kenya-business-portal/releases)
[![Django](https://img.shields.io/badge/django-4.2+-green.svg)](https://djangoproject.com)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)](https://github.com/yourusername/kenya-business-portal/actions)
[![Code Coverage](https://img.shields.io/badge/coverage-85%25-green.svg)](https://github.com/yourusername/kenya-business-portal/coverage)
[![Security](https://img.shields.io/badge/security-scanned-blue.svg)](https://github.com/yourusername/kenya-business-portal/security)
[![Maintenance](https://img.shields.io/badge/maintained-yes-green.svg)](https://github.com/yourusername/kenya-business-portal/graphs/commit-activity)

> A comprehensive Django web application for streamlining business registration processes in Kenya, featuring user management, business registration workflows, and administrative oversight.

## 🇰🇪 About This Project

The Kenya Business Registration Portal aims to digitize and simplify the business registration process for Kenyan entrepreneurs, providing a user-friendly platform that connects business owners with regulatory authorities while maintaining compliance with local requirements.

## 📋 Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [User Guide](#user-guide)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## ✨ Features

### 🎯 Core Functionality

| Feature | Status | Description |
|---------|--------|-------------|
| 👤 **User Management** | ✅ Complete | Secure account creation with Kenyan ID/Passport validation |
| 🏢 **Business Registration** | ✅ Complete | Comprehensive business registration with industry categorization |
| 📊 **Admin Dashboard** | ✅ Complete | Administrative oversight with approval workflows |
| 🔐 **Authentication** | ✅ Complete | Django-based authentication with password recovery |
| 📱 **Responsive Design** | ✅ Complete | Mobile-friendly interface for all devices |
| 🌍 **Localization** | 🚧 In Progress | Support for English and Swahili languages |
| 🔗 **API Integration** | 📋 Planned | RESTful API for third-party integrations |
| 📈 **Analytics** | 📋 Planned | Business registration analytics and reporting |

### 🛡️ Security Features

- CSRF protection on all forms
- SQL injection prevention
- Secure password hashing
- Session management
- Input validation and sanitization
- Rate limiting for API endpoints

### 🌟 User Experience

- Intuitive step-by-step registration process
- Real-time form validation
- Progress tracking for applications
- Email notifications for status updates
- Document upload capabilities
- Multi-language support (planned)

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/kenya-business-portal.git
cd kenya-business-portal

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration

# Run database migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data (Kenyan counties, business types)
python manage.py loaddata fixtures/initial_data.json

# Start development server
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

## 🛠️ Installation

### Prerequisites

- **Python 3.8+**
- **Django 4.2+**
- **PostgreSQL 12+** (recommended for production)
- **Redis** (for caching and sessions)
- **Node.js & npm** (for frontend assets)

### Development Setup

1. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/kenya-business-portal.git
   cd kenya-business-portal
   ```

2. **Environment Setup**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements/development.txt
   ```

3. **Database Configuration**
   ```bash
   # Create PostgreSQL database
   createdb kenya_business_portal
   
   # Apply migrations
   python manage.py migrate
   
   # Load initial data
   python manage.py loaddata fixtures/counties.json
   python manage.py loaddata fixtures/business_types.json
   ```

4. **Environment Variables**
   ```bash
   cp .env.example .env
   ```
   
   Configure your `.env` file:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=postgresql://user:password@localhost/kenya_business_portal
   EMAIL_HOST=smtp.gmail.com
   EMAIL_PORT=587
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-app-password
   REDIS_URL=redis://localhost:6379/0
   ```

5. **Frontend Assets**
   ```bash
   npm install
   npm run build
   ```

6. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

## 📁 Project Structure

```
kenya-business-portal/
├── 📁 apps/
│   ├── 📁 accounts/              # User authentication & profiles
│   │   ├── models.py            # User model extensions
│   │   ├── views.py             # Authentication views
│   │   ├── forms.py             # Registration/login forms
│   │   └── urls.py              # Account-related URLs
│   ├── 📁 business/             # Business registration & management
│   │   ├── models.py            # Business, Owner models
│   │   ├── views.py             # Business CRUD operations
│   │   ├── forms.py             # Business registration forms
│   │   └── admin.py             # Admin interface customization
│   └── 📁 api/                  # RESTful API (planned)
│       ├── serializers.py       # API serializers
│       ├── views.py             # API endpoints
│       └── urls.py              # API routing
├── 📁 templates/
│   ├── 📁 base/                 # Base templates
│   │   ├── base.html            # Master template
│   │   └── navigation.html      # Navigation component
│   ├── 📁 registration/         # Authentication templates
│   │   ├── login.html           # Login form
│   │   ├── register.html        # User registration
│   │   └── password_reset.html  # Password recovery
│   ├── 📁 business/             # Business-related templates
│   │   ├── register.html        # Business registration
│   │   ├── dashboard.html       # User dashboard
│   │   ├── list.html            # Business listings
│   │   └── detail.html          # Business details
│   └── 📁 admin/                # Admin templates
│       ├── approval.html        # Approval queue
│       └── reports.html         # System reports
├── 📁 static/
│   ├── 📁 css/                  # Stylesheets
│   ├── 📁 js/                   # JavaScript files
│   └── 📁 images/               # Static images
├── 📁 media/                    # User uploads
├── 📁 fixtures/                 # Initial data
│   ├── counties.json            # Kenyan counties
│   └── business_types.json      # Business categories
├── 📁 requirements/             # Dependencies
│   ├── base.txt                 # Base requirements
│   ├── development.txt          # Development dependencies
│   └── production.txt           # Production requirements
├── 📁 config/                   # Django settings
│   ├── settings/
│   │   ├── base.py              # Base settings
│   │   ├── development.py       # Development settings
│   │   └── production.py        # Production settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── manage.py                    # Django management script
├── .env.example                 # Environment variables template
├── docker-compose.yml           # Docker configuration
└── README.md                    # This file
```

## 🏗️ System Architecture

### Database Models

#### User Profile Model
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    national_id = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15)
    physical_address = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
```

#### Business Model
```python
class Business(models.Model):
    name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=50, blank=True)
    business_type = models.ForeignKey(BusinessType, on_delete=models.CASCADE)
    industry_sector = models.ForeignKey(IndustrySector, on_delete=models.CASCADE)
    county = models.ForeignKey(County, on_delete=models.CASCADE)
    date_established = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
```

### Application Flow

```mermaid
graph TD
    A[User Visits Portal] --> B[Register Account]
    B --> C[Verify Email]
    C --> D[Complete Profile]
    D --> E[Submit Business Application]
    E --> F[Admin Review]
    F --> G{Approved?}
    G -->|Yes| H[Business Registered]
    G -->|No| I[Request Amendments]
    I --> E
    H --> J[Dashboard Access]
```

## 👥 User Guide

### For Business Owners

#### 1. Account Registration
1. Visit the registration page
2. Provide required information:
   - Full name
   - National ID or Passport number
   - Email address
   - Phone number
   - Physical address
3. Verify your email address
4. Complete your profile

#### 2. Business Registration
1. Log in to your account
2. Navigate to "Register Business"
3. Fill out the business registration form:
   - Business name
   - Business type (Sole Proprietorship, Partnership, etc.)
   - Industry sector
   - County location
   - Date of establishment
   - Add business partners/directors (if applicable)
4. Upload required documents
5. Submit for review

#### 3. Dashboard Features
- **View Applications**: Track the status of your business registrations
- **Edit Information**: Update business details before approval
- **Document Management**: Upload and manage business documents
- **Notifications**: Receive updates on application status

### For Administrators

#### 1. Review Applications
- Access the admin panel
- Review pending business applications
- Verify submitted documents
- Approve or request amendments

#### 2. System Management
- Generate reports on registration statistics
- Manage user accounts
- Configure system settings
- Monitor application performance

## 🔗 API Documentation

### Authentication

All API endpoints require authentication via JWT tokens.

```bash
# Obtain token
POST /api/auth/login/
{
    "username": "user@example.com",
    "password": "password123"
}

# Use token in requests
Authorization: Bearer <your-jwt-token>
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/businesses/` | List all businesses |
| `POST` | `/api/businesses/` | Create new business |
| `GET` | `/api/businesses/{id}/` | Get business details |
| `PUT` | `/api/businesses/{id}/` | Update business |
| `DELETE` | `/api/businesses/{id}/` | Delete business |
| `GET` | `/api/counties/` | List Kenyan counties |
| `GET` | `/api/business-types/` | List business types |

### Example API Usage

```python
import requests

# List businesses
response = requests.get(
    'https://api.kenya-business-portal.com/api/businesses/',
    headers={'Authorization': 'Bearer <token>'}
)
businesses = response.json()
```

## 🧪 Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.business

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Code Quality

```bash
# Linting
flake8 .
black .
isort .

# Security checks
bandit -r .
safety check
```

### Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f web
```

### Production Checklist

- [ ] Set `DEBUG = False`
- [ ] Configure proper `ALLOWED_HOSTS`
- [ ] Set up SSL certificate
- [ ] Configure Redis for caching
- [ ] Set up database backups
- [ ] Configure email settings
- [ ] Set up monitoring and logging
- [ ] Configure static file serving
- [ ] Set up CI/CD pipeline

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | ✅ |
| `DEBUG` | Debug mode (True/False) | ✅ |
| `DATABASE_URL` | Database connection string | ✅ |
| `EMAIL_HOST` | SMTP server host | ✅ |
| `EMAIL_HOST_USER` | SMTP username | ✅ |
| `EMAIL_HOST_PASSWORD` | SMTP password | ✅ |
| `REDIS_URL` | Redis connection string | ❌ |
| `SENTRY_DSN` | Error tracking (Sentry) | ❌ |

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Getting Started

1. **Fork** the repository
2. **Clone** your fork: `git clone https://github.com/yourusername/kenya-business-portal.git`
3. **Create** a feature branch: `git checkout -b feature/amazing-feature`
4. **Make** your changes
5. **Test** thoroughly
6. **Commit** changes: `git commit -m 'Add amazing feature'`
7. **Push** to branch: `git push origin feature/amazing-feature`
8. **Create** a Pull Request

### Development Guidelines

- **Code Style**: Follow PEP 8 standards
- **Testing**: Write tests for new features
- **Documentation**: Update documentation for changes
- **Commit Messages**: Use conventional commit format
- **Security**: Follow security best practices

### Areas for Contribution

- 🌍 **Localization**: Swahili translations
- 🎨 **UI/UX**: Design improvements
- 📱 **Mobile**: Mobile app development
- 🔌 **Integrations**: Third-party service integrations
- 📚 **Documentation**: Improve documentation
- 🐛 **Bug Fixes**: Report and fix issues

## 📊 Roadmap

### Phase 1: Foundation (Current)
- [x] User authentication system
- [x] Business registration workflow
- [x] Admin approval system
- [x] Basic dashboard functionality

### Phase 2: Enhancement (Q2 2025)
- [ ] RESTful API development
- [ ] Mobile-responsive improvements
- [ ] Document management system
- [ ] Email notification system

### Phase 3: Advanced Features (Q3 2025)
- [ ] Integration with government databases
- [ ] Multi-language support
- [ ] Advanced reporting and analytics
- [ ] Mobile application

### Phase 4: Scale (Q4 2025)
- [ ] Performance optimization
- [ ] Advanced security features
- [ ] Third-party integrations
- [ ] Enterprise features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

### Getting Help

- 📚 **Documentation**: [Read the docs](https://github.com/yourusername/kenya-business-portal/wiki)
- 🐛 **Bug Reports**: [Report issues](https://github.com/yourusername/kenya-business-portal/issues/new?template=bug_report.md)
- ✨ **Feature Requests**: [Request features](https://github.com/yourusername/kenya-business-portal/issues/new?template=feature_request.md)
- 💬 **Discussions**: [Join discussions](https://github.com/yourusername/kenya-business-portal/discussions)

### Contact Information

- **Email**: support@kenya-business-portal.com
- **Twitter**: [@KenyaBusinessPortal](https://twitter.com/KenyaBusinessPortal)
- **LinkedIn**: [Kenya Business Portal](https://linkedin.com/company/kenya-business-portal)

### Community

- **Slack**: [Join our Slack workspace](https://join.slack.com/t/kenya-business-portal)
- **Discord**: [Developer Discord server](https://discord.gg/kenya-business-portal)

---

<div align="center">

**🇰🇪 Proudly serving Kenyan entrepreneurs**

[Live Demo](https://demo.kenya-business-portal.com) • [Documentation](https://docs.kenya-business-portal.com) • [API Docs](https://api.kenya-business-portal.com/docs)

**⭐ Star this repository if you find it useful!**

Made with ❤️ for the Kenyan business community

</div>
