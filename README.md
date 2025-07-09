## SparkEd FLASK Application

Welcome to the SparkEd secure login/registration Application! This is a registration and login web app built with Flask, designed to provide a secure and user-friendly platform. It features user registration, login, email verification, and a basic dashboard.

## ✨ Features

*   **User Authentication:** Secure registration and login system.
*   **Email Verification:** Ensures valid user emails through a confirmation process.
*   **User Dashboard:** A personalized page displaying user information.
*   **Database Integration:** Uses PostgreSQL for robust data storage.
*   **Dockerized Environment:** Easy setup and deployment using Docker and Docker Compose.
*   **Secure Forms:** Integration with Cloudflare Turnstile for bot protection.

## 🚀 Technologies Used

*   **Flask:** A lightweight Python web framework.
*   **SQLAlchemy:** A powerful SQL toolkit and Object-Relational Mapper (ORM) for database interactions.
*   **PostgreSQL:** A robust, open-source relational database system.
*   **Docker & Docker Compose:** Containerization and orchestration tools for managing services.
*   **python-dotenv:** For managing environment variables.
*   **Flask-WTF:** Simple integration of WTForms with Flask for handling web forms.
*   **Requests:** A popular Python library for making HTTP requests (used here for Turnstile verification).
*   **Cloudflare Turnstile:** A smart CAPTCHA alternative for verifying human visitors.
*   **SMTP:** For sending email confirmations.
*   **Werkzeug:** A comprehensive WSGI web application library (used for password hashing).
*   **HTML, CSS, JavaScript:** Frontend development.
*   **Jinja2:** Flask's default templating engine.
*   **Gunicorn:** A Python WSGI HTTP Server for UNIX (used for running the Flask app in production/Docker).

## 🏗️ Project Structure

The project is organized as follows:

```
.
├── app.py                # Main Flask application file
├── database_init.py      # Script for database initialization
├── dbm.py                # Database management operations (CRUD)
├── docker-compose.yaml   # Defines and manages multi-container Docker applications
├── smtp.py               # Email sending functionality
├── .env                  # Environment variables
├── .gitignore            # Specifies intentionally untracked files that Git should ignore
├── Dockerfile            # Defines the Docker image for the Flask application
├── requirements.txt      # Lists Python dependencies
├── static/               # Static files (CSS, JS, Images)
│   ├── css/
│   ├── img/
│   └── js/
└── templates/            # HTML templates
    ├── base.html
    ├── confirmation.html
    ├── dashboard.html
    ├── login.html
    ├── register.html
    └── welcome.html
```

## ⚙️ How it Works

The application follows a standard Flask web architecture. `app.py` handles routing and request processing. It interacts with `dbm.py` to perform database operations using SQLAlchemy, connecting to a PostgreSQL database. User authentication involves password hashing (using Werkzeug) and session management. Email verification is handled asynchronously via `smtp.py` and uses `itsdangerous` for secure token generation. Cloudflare Turnstile is integrated into the registration and login forms for bot protection. The frontend is built using HTML templates rendered by Jinja2, styled with CSS, and enhanced with JavaScript. Docker Compose (in the first setup method) orchestrates the database and the Flask application.

## 🚀 Getting Started

You can set up and run this project using two different methods:

### Method 1: Setup with Docker Compose (Recommended)

This method uses Docker Compose to manage both the database and the Flask application containers.

#### Prerequisites

*   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/)
*   A Cloudflare account to get Turnstile site and secret keys.
*   An email account (like Gmail) to configure SMTP settings.

#### Setup Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/bennetsharwin/SparkEd-secure-flask-app.git
    cd SparkEd-secure-flask-app
    ```

2.  **Create and configure the `.env` file:**

    Create a file named `.env` in the root directory of the project. Copy the contents from `.env.example` (you might need to create this file manually based on the variables used in `app.py` and `dbm.py`) and fill in your credentials and keys. **Keep this file secure**

    Your `.env` file should look something like this (replace placeholders with your actual values):

    ```dotenv
    SECRET_KEY=YOUR_SECRET_KEY
    DB_HOST=db # This should match the service name in docker-compose.yaml
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    DB_NAME=your_db_name

    # SMTP Configuration (Example for Gmail)
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=465
    MAIL_USERNAME=your_email@gmail.com
    MAIL_PASSWORD=your_email_app_password # Use an app password for Gmail
    MAIL_USE_TLS=False
    MAIL_USE_SSL=True

    # Application Configuration
    FLASK_ENV=development # or production
    HOST=localhost # or your domain/IP
    PROTOCOL=http # or https

    # Turnstile Credentials
    CF_TURNSTILE_SECRETKEY=YOUR_TURNSTILE_SECRET_KEY
    CF_TURNSTILE_SITEKEY=YOUR_TURNSTILE_SITE_KEY
    ```

3.  **Build and run the Docker containers:**

    Navigate to the project root directory in your terminal and run:

    ```bash
    docker-compose up --build -d
    ```
    The `-d` flag runs the containers in detached mode.

4.  **Initialize the database:**

    Once the database container is running, you need to initialize the database schema. Execute the `database_init.py` script inside the running `flask_app` container:

    ```bash
    docker exec <flask_container_id> python database_init.py
    ```
    Replace `<flask_container_id>` with the actual ID of your running Flask container (you can find it using `docker ps`).

5.  **Access the application:**

    The Flask application should be running on `http://localhost:5000`

### Method 2: Setup without Docker Compose (Database in Docker)

This method runs the Flask application directly on your host machine while using a Docker container for the PostgreSQL database.

#### Prerequisites

*   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
*   [Docker](https://docs.docker.com/get-docker/)
*   [Python 3.12+](https://www.python.org/downloads/)
*   A Cloudflare account to get Turnstile site and secret keys.
*   An email account (like Gmail) to configure SMTP settings.

#### Setup Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/bennetsharwin/SparkEd-secure-flask-app.git
    cd SparkEd-secure-flask-app
    ```

2.  **Create and configure the `.env` file:**

    Create a file named `.env` in the root directory of the project as described in Method 1. This file will be used by your locally running Flask application.

3.  **Run the PostgreSQL database in Docker:**

    Use the following command to run a PostgreSQL container. This command exposes the database port (5432) on your host machine and uses a named volume for persistent data.

    ```bash
    docker run --name spark_ed_db -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydatabase -p 5432:5432 -v db_data:/var/lib/postgresql/data -d postgres:latest
    ```
    *   `--name spark_ed_db`: Assigns a name to the container.
    *   `-e ...`: Sets environment variables for the database credentials and database name.
    *   `-p 5432:5432`: Maps port 5432 on your host to port 5432 in the container.
    *   `-v db_data:/var/lib/postgresql/data`: Uses a named volume for data persistence.
    *   `-d`: Runs the container in detached mode.
    *   `postgres:latest`: Specifies the Docker image to use.

4.  **Set up the Python virtual environment and install dependencies:**

    It's highly recommended to use a virtual environment to manage dependencies.

    ```bash
    python -m venv venv
    .\venv\Scripts\activate # On Windows
    # source venv/bin/activate # On macOS/Linux
    pip install -r requirements.txt
    ```

5.  **Initialize the database:**

    With the database container running and your virtual environment activated, run the database initialization script:

    ```bash
    python database_init.py
    ```
    Ensure your `.env` file is correctly configured to point to `DB_HOST=localhost` (since the database port is exposed on the host).

6.  **Run the Flask application:**

    With your virtual environment activated, you can run the Flask application using gunicorn:

    ```bash
    gunicorn --bind 0.0.0.0:5000 app:app
    ```
    *Note: Gunicorn is primarily for UNIX-like systems. If you are on Windows, you might need to use Flask's built-in development server instead.*

    Or for development with Flask's built-in server:

    ```bash
    flask run
    ```

7.  **Access the application:**

    The Flask application should be running on `http://localhost:5000`.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any bugs or feature requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---