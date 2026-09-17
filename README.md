# Pharmacy Management System

A Flask-based pharmacy management application for managing medicines, customers, prescriptions, bills, and reports. The project uses MySQL as the database backend and includes both a browser-based web interface and a terminal-based CLI workflow.

## Project Overview

This application provides:

- Medicine inventory management
- Customer management
- Prescription tracking
- Billing and invoice generation
- Low-stock and exportable reports
- User login using Flask-Login

## Project Structure

```text
pharmacy/
├── app.py                  # Flask web application entry point
├── main.py                 # Terminal/CLI application entry point
├── requirements.txt        # Python dependencies
├── exceptions.py           # Custom exceptions
├── dao/                    # Data access objects for database operations
├── database/               # DB configuration and connection setup
├── models/                 # Domain model classes
├── repositories/           # Repository layer for DB queries
├── services/               # Business logic layer
├── templates/              # Jinja2 HTML templates
├── static/                 # Optional static files (CSS/JS/images)
└── .env                    # Local environment variables (not committed)
```

## Tech Stack

- Python 3.10+
- Flask 3.0.2
- Flask-Login 0.6.3
- MySQL Connector Python
- Pandas + OpenPyXL for Excel reporting
- Jinja2 templates

## Prerequisites

Before running the project, install:

- Python 3.10 or newer
- MySQL Server
- A MySQL database named `pharmacy_db` (or change the environment values)
- pip (Python package installer)

## Environment Configuration

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=pharmacy_db
DB_USER=root
DB_PASSWORD=root
SECRET_KEY=change_this_secret_key
```

If you are using a different MySQL setup, update these values accordingly.

## Installation

From the project root:

```bash
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```

### macOS/Linux

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Database Setup

Make sure MySQL is running, then create the database:

```sql
CREATE DATABASE pharmacy_db;
```

You may also need to create the required tables, depending on your database setup. The app expects tables such as:

- `users`
- `medicines`
- `customers`
- `prescriptions`
- `prescription_medicines`
- `bills`
- `bill_items`

A typical `users` table for login looks like:

```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    role VARCHAR(50) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
```

## Creating an Initial Admin User

Because the app uses Flask-Login and password hashing, create a user record before logging in. Example:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('admin123'))"
```

Then insert it into MySQL:

```sql
INSERT INTO users (username, role, password_hash)
VALUES ('admin', 'admin', 'GENERATED_HASH_FROM_ABOVE');
```

You can then log in with:

- Username: `admin`
- Password: `admin123`

## Run the Web Application

Start the Flask app:

```bash
python app.py
```

Then open:

```text
http://localhost:5000/login
```

The app is configured to run in debug mode by default.

## Run the CLI Application

The project also includes a terminal-based system in `main.py`:

```bash
python main.py
```

This menu-based app supports:

- Medicine management
- Customer management
- Prescription management
- Billing
- Reports

## Main Web Routes

The Flask app exposes these routes:

- `/login` - Login page
- `/logout` - Logout
- `/` - Home/dashboard (requires login)
- `/medicines` - View medicine inventory
- `/medicines/add` - Add a medicine
- `/customers` - Customer list and search
- `/prescriptions` - Prescription search/filter
- `/bills` - Bill search/filter
- `/reports` - Reports page
- `/reports/low-stock` - Low-stock inventory report

## Common Commands

### Install dependencies

```bash
pip install -r requirements.txt
```

### Activate virtual environment

Windows:

```powershell
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### Run the server

```bash
python app.py
```

### Run the CLI

```bash
python main.py
```

### Upgrade pip packages (optional)

```bash
pip install --upgrade pip
```

## Notes

- The application expects a working MySQL connection at startup.
- Some functionality is implemented in the DAO layer and may require the relevant MySQL tables to already exist.
- The low-stock report can export to Excel using pandas/openpyxl.
- The project uses a layered structure: models -> DAO -> repositories -> services -> Flask routes.

## Troubleshooting

### MySQL connection errors

Check that:

- MySQL is running
- Your `.env` values are correct
- The database exists
- The user has permission to access it

### Login fails

Ensure:

- A user exists in the `users` table
- The `password_hash` was generated correctly
- You are using the right password when logging in

### Module import errors

Reinstall dependencies and confirm the virtual environment is active:

```bash
pip install -r requirements.txt
```

## License

This project is provided as a local academic or personal project and does not include a specific license file unless added later.
