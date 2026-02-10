# WebDevelopment

A Flask web application with user authentication, customer management, and course management features.

## Features

- User authentication (login/register)
- Customer management (CRUD operations)
- Course management (CRUD operations)
- Docker support for easy deployment

## Tech Stack

- **Backend:** Python, Flask, Flask-SQLAlchemy
- **Database:** MySQL (via PyMySQL)
- **Frontend:** HTML, CSS, Jinja2 templates
- **Deployment:** Docker, Docker Compose

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/WebDevelopment.git
cd WebDevelopment
```

2. Create a virtual environment:
```bash
python -m venv virtual
source virtual/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python app.py
```

## Docker Deployment

```bash
docker-compose up --build
```

## Project Structure

```
├── app.py              # Main Flask application
├── config.py           # Configuration settings
├── db_setup.py         # Database setup script
├── requirements.txt    # Python dependencies
├── Dockerfile          # Docker image definition
├── docker-compose.yml  # Docker Compose configuration
├── static/             # Static files (CSS, images)
│   └── css/           # Stylesheets
├── templates/          # HTML templates
│   ├── courses/       # Course management templates
│   ├── customers/     # Customer management templates
│   └── ...
└── .env               # Environment variables (local only)
```

## License

MIT

