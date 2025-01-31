# Prashnavali (प्रश्नावली)

A comprehensive multilingual FAQ management system built with Django Rest Framework. Prashnavali, meaning "collection of questions" in Sanskrit, is designed to handle frequently asked questions with seamless support for multiple languages including English, Hindi, and Bengali.

## Features

- Multilingual FAQ management system with support for:
  - English (Default)
  - Hindi (हिंदी)
  - Bengali (বাংলা)
- Rich text editing with WYSIWYG editor support using CKEditor
- Automated translation using Google Translate API
- High-performance Redis-based caching system
- RESTful API with language selection capabilities
- Docker support for seamless deployment

## Prerequisites

- Python 3.9+
- Redis
- Docker (optional)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
Create a `.env` file in the project root and add:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Docker Installation

1. Build and run using Docker Compose:
```bash
docker-compose up --build
```

## API Usage

### Get FAQs

```bash
# Get FAQs in English (default)
curl http://localhost:8000/api/faqs/

# Get FAQs in Hindi (हिंदी)
curl http://localhost:8000/api/faqs/?lang=hi

# Get FAQs in Bengali (বাংলা)
curl http://localhost:8000/api/faqs/?lang=bn
```

### Create FAQ

```bash
curl -X POST http://localhost:8000/api/faqs/ \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Prashnavali?", "answer": "Prashnavali is a multilingual FAQ management system."}'
```

## Testing

Run tests using pytest:
```bash
pytest
```

## Admin Interface

Access the admin interface at `http://localhost:8000/admin/` to:
- Create and manage FAQs
- View and edit translations
- Monitor the system

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Status

Prashnavali is actively maintained and welcomes contributions from the community. For any issues or suggestions, please open an issue in the repository.