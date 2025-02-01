# Prashnavali

A Django-based FAQ management system with multi-language support, featuring automatic translations, WYSIWYG editing capabilities, and efficient caching mechanisms.

## Features

- Multi-language support for:
  - English (en)
  - Hindi (hi)
  - Bengali (bn)
  - Gujarati (gu)
  - Punjabi (pa)
- Rich text editing with CKEditor integration
- Automatic translation using `googletrans` library
- Redis-based caching system
- RESTful API with language parameter support
- Comprehensive test coverage using pytest
- Docker and Docker Compose support for development and deployment

## Tech Stack

### Core Technologies
- Python 3.9
- Django 5.1
- Django REST Framework
- Redis (for caching)

### Dependencies
- django-ckeditor (for WYSIWYG editor)
- googletrans (for automatic translations)
- pytest (for testing)
- gunicorn (for production deployment)

### Development & Deployment
- Docker
- Docker Compose
- flake8 (for code linting)

## Prerequisites

- Python 3.9 or higher
- Redis Server 6.0 or higher
- Docker and Docker Compose (for containerized deployment)
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SakshamTolani/Prashnavali
cd prashnavali
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run database migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Start Redis server (if not running):
```bash
redis-server
```

## API Documentation

### FAQ Endpoints

#### List FAQs
```
GET /api/faqs/
```

Query Parameters:
- `lang`: Language code (Optional)
  - Supported values: en, hi, bn, gu, pa
  - Default: en

Example Requests:
```bash
# Get FAQs in default language (English)
curl http://localhost:8000/api/faqs/

# Get FAQs in Hindi
curl http://localhost:8000/api/faqs/?lang=hi

# Get FAQs in Bengali
curl http://localhost:8000/api/faqs/?lang=bn
```

Example Response:
```json
[
    {
        "id": 1,
        "question": "What is Django?",
        "answer": "Django is a high-level Python web framework.",
        "created_at": "2024-02-01T10:00:00Z",
        "updated_at": "2024-02-01T10:00:00Z"
    }
]
```

#### Create FAQ
```
POST /api/faqs/
```

Request Body:
```json
{
    "question": "What is Django?",
    "answer": "Django is a high-level Python web framework."
}
```

Notes:
- Translations are automatically generated using googletrans
- Rich text formatting is supported in the answer field
- The system automatically caches the created FAQ and its translations

#### Update FAQ
```
PUT /api/faqs/{id}/
```

#### Delete FAQ
```
DELETE /api/faqs/{id}/
```

## Translation System

The system uses the `googletrans` library for automatic translations:

- Translations are generated automatically when a new FAQ is created
- Supported languages: Hindi, Bengali, Gujarati, and Punjabi
- Translation process:
  1. Original text is saved in English
  2. System attempts automatic translation
  3. If translation fails, falls back to English
  4. Successful translations are cached

### Translation Fields
Each FAQ entry contains the following translation fields:
```python
question_hi: Hindi question
answer_hi: Hindi answer
question_bn: Bengali question
answer_bn: Bengali answer
question_gu: Gujarati question
answer_gu: Gujarati answer
question_pa: Punjabi question
answer_pa: Punjabi answer
```

## Caching System

Redis-based caching implementation:

### Cache Configuration
- FAQ list cache: 15 minutes (configurable via `CACHE_TIMEOUT`)
- Translation cache: 24 hours
- Cache keys format: `faq_{id}_{field}_{lang}`

### Cache Operations
- Cache invalidation occurs on:
  - FAQ updates
  - Manual cache clearing
  - Timeout expiration
- Fallback to database if cache miss occurs
- Automatic cache repopulation on miss

## Testing

Run the complete test suite:
```bash
pytest
```

Run specific test categories:
```bash
pytest test_faq_api.py  # API tests only
pytest -k "test_cache"  # Cache-related tests only
```

### Test Coverage
The test suite covers:
- FAQ CRUD operations
- Translation functionality
- Caching mechanisms
- API endpoints
- Language fallback behavior
- Error handling
- Model methods

## Project Structure

```
prashnavali/
├── base/
│   ├── __init__.py
│   ├── models.py          # FAQ model with translation support
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # ViewSet implementations
│   └── tests/
│       ├── __init__.py
│       └── test_faq_api.py
├── backend/
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py           # URL configurations
│   └── wsgi.py
├── docker/
│   ├── Dockerfile
│   └── entrypoint.sh
├── .env.example
├── .gitignore
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

## Environment Variables

Required environment variables:
```
DEBUG=True/False
SECRET_KEY=your-secret-key
REDIS_URL=redis://redis:6379/0
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Optional settings:
```
CACHE_TIMEOUT=900  # Cache timeout in seconds (default: 15 minutes)
DEFAULT_LANGUAGE=en  # Default language for FAQs
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Run tests
5. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Coding Standards
- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings for all functions and classes
- Include type hints where appropriate
- Write unit tests for new features

### Commit Message Format
```
type: Subject

Body (optional)

Footer (optional)
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding or modifying tests
- chore: Maintenance tasks

## Troubleshooting

### Common Issues

1. Translation Service Issues:
```
Issue: Translations not working
Solution: 
- Check internet connectivity
- Verify googletrans version compatibility
- System will automatically fall back to English
```

2. Redis Connection:
```
Issue: Redis connection failing
Solution:
- Check if Redis server is running
- Verify Redis connection settings
- Ensure correct Redis port is accessible
```

3. CKEditor Integration:
```
Issue: WYSIWYG editor not loading
Solution:
- Verify static files are collected
- Check JavaScript console for errors
- Ensure CKEditor configuration is correct
```

## Performance Considerations

- Redis caching reduces database load
- API responses are cached for 15 minutes
- Translations are cached for 24 hours
- Database queries are optimized
- Static files are served through CDN in production

## Security

- CSRF protection enabled
- XSS protection via Django's template system
- SQL injection protection
- Rate limiting on API endpoints
- Secure cookie handling

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support:
1. Check existing documentation
2. Search through Issues
3. Create a new Issue with:
   - Detailed description
   - Steps to reproduce
   - Environment details
   - Error messages/logs
   - Expected vs actual behavior

## Acknowledgments

- Django REST Framework for API functionality
- CKEditor for rich text editing
- googletrans for translation services
- Redis for caching support