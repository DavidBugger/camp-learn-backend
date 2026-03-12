# CampLearn Backend

CampLearn is an offline-first digital learning platform designed to provide high-quality education to children and youth in IDP (Internally Displaced Persons) camps and underserved communities. This repository contains the Django-based backend API.

## 🚀 Features

- **RBAC (Role-Based Access Control):** Granular permissions for Students, Facilitators, Camp Admins, and System Admins.
- **Learning Content Management:** Comprehensive management of Courses and Lessons (Video, Audio, Text).
- **Assessment Engine:** Integrated Quiz system with automated grading.
- **Progress Tracking:** Real-time tracking of learner progress through courses and lessons.
- **Gamification:** Points, Badges, and Leaderboard system to drive engagement.
- **Offline Sync:** Architecture designed to synchronize offline activity logs from local learning hubs to the cloud.
- **Impact Analytics:** Advanced reporting on camp performance and learner engagement metrics.
- **Auto-Generated Docs:** Interactive API documentation via Swagger/OpenAPI.

## 🛠 Tech Stack

- **Framework:** [Django 4.2 LTS](https://www.djangoproject.com/)
- **API Engine:** [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- **Authentication:** [SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- **Documentation:** [drf-spectacular](https://github.com/tfranzel/drf-spectacular) (OpenAPI 3.0)
- **Environment Management:** [Python Decouple](https://github.com/HBNetwork/python-decouple)
- **Database:** PostgreSQL (Production recommended), SQLite (Development default)

## 📋 Prerequisites

- Python 3.9+
- pip
- virtualenv

## ⚙️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CAMPLEARN
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your local settings (SECRET_KEY, DB settings, etc.)
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

## 🏃 Running the Application

Start the development server:
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`.

## 📖 Documentation

- **Swagger UI:** [http://127.0.0.1:8000/api/docs/](http://127.0.0.1:8000/api/docs/)
- **Django Admin:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 🧪 Testing

The project includes an end-to-end integration test suite. Run tests using:
```bash
python manage.py test apps.core_integration_test -v 2
```

## 📂 Project Structure

```
CAMPLEARN/
├── apps/
│   ├── accounts/     # Authentication & User Profiles
│   ├── camps/        # Camp & Location Management
│   ├── courses/      # Learning Content & Lessons
│   ├── quizzes/      # Assessments & Grading
│   ├── progress/     # Learner Progress Tracking
│   ├── gamification/ # Points & Badges Engine
│   ├── devices/      # Sync & Device Management
│   └── analytics/    # Impact & Usage Reporting
├── config/           # Project Settings & Root URLs
└── utils/            # Shared helper functions
```

## 📄 License

This project is licensed under the MIT License.
