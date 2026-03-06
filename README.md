# CSE-25-02-ST-ASSESSMENT

Django E-commerce application with CI/CD pipeline for Render deployment.

## Project Structure

```
CSE-25-02-ST-ASSESSMENT/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD pipeline
├── Orena_Gideon/
│   ├── E_commerce/            # Django project
│   ├── requirements.txt        # Python dependencies
│   └── Procfile              # Render deployment configuration
├── render.yaml               # Render service configuration
└── README.md
```

## Deployment Pipeline

This project uses GitHub Actions for CI/CD with the following workflow:

1. **Test Stage** (on push to any branch):
   - Sets up Python 3.11
   - Installs dependencies
   - Runs Django tests
   - Runs Django deployment checks

2. **Deploy Stage** (on push to main branch only):
   - Deploys to Render if tests pass
   - Uses Render API for automatic deployment

## Setup Instructions

### 1. GitHub Secrets
Add these secrets to your GitHub repository:

- `RENDER_API_KEY`: Your Render API key
- `RENDER_SERVICE_ID`: Your Render service ID

### 2. Render Configuration
The `render.yaml` file configures:
- Python 3.11 environment
- Automatic deployment on push to main
- Environment variables for production
- Build and start commands

### 3. Local Development

```bash
# Navigate to project
cd Orena_Gideon/E_commerce

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r ../../requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Environment Variables

The application uses these environment variables:

- `SECRET_KEY`: Django secret key (auto-generated in production)
- `DEBUG`: Debug mode (set to 'false' in production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `PYTHON_VERSION`: Python version (3.11)
- `DJANGO_SETTINGS_MODULE`: Django settings module

## Production Features

- **Security**: Environment-based configuration, secure headers
- **Static Files**: Whitenoise for efficient static file serving
- **Web Server**: Gunicorn WSGI server
- **Database**: SQLite (can be upgraded to PostgreSQL in production)
- **CI/CD**: Automated testing and deployment

## Deployment to Render

1. Push your code to the main branch
2. GitHub Actions will automatically run tests
3. If tests pass, the app will be deployed to Render
4. Monitor deployment in GitHub Actions tab

## Testing

Run tests locally:

```bash
cd Orena_Gideon/E_commerce
python manage.py test
```

Run Django deployment checks:

```bash
python manage.py check --deploy
```
