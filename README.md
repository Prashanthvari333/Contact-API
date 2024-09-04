# Phone Number Lookup API

This project is a REST API built using Django for a mobile app that allows users to search for a person's name by phone number and mark numbers as spam. The API is designed for production-level performance, security, and scalability.

## Features

- **User Registration & Login**: Users can register with a name, phone number, and password. Login is required to access any features.
- **Spam Marking**: Users can mark a phone number as spam to help others identify spam callers.
- **Search Functionality**: 
  - Search by name: Returns matching results, displaying the name, phone number, and spam likelihood.
  - Search by phone number: Shows the associated name(s) and spam likelihood.
- **Profile Management**: Users can view their profile and update their information.
- **Data Security**: Ensures that email addresses are only visible to authorized users.

## Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: MySQL
- **ORM**: Django ORM
- **Authentication**: Token-based authentication using Django Rest Framework's TokenAuthentication.

## Getting Started

### Prerequisites

- Python 3.x
- MySQL
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/phone-number-lookup-api.git
    cd phone-number-lookup-api
    ```

2. **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows use `venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the database**:
    - Update the `DATABASES` setting in `settings.py` with your PostgreSQL credentials.

5. **Apply migrations**:
    ```bash
    python manage.py migrate
    ```

6. **Create a superuser** (for accessing the Django admin panel):
    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

### API Endpoints

- **Register**: `POST /api/register/`
- **Login**: `POST /api/login/`
- **Mark Number as Spam**: `POST /api/spam/`
- **Search by Name**: `GET /api/search/name/`
- **Search by Phone Number**: `GET /api/search/phone/`
- **View Profile**: `GET /api/profile/`

### Testing

You can populate the database with sample data for testing by running the custom management command:

```bash
python manage.py generate_data
```
