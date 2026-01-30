# Project Setup and Run Guide

This guide provides comprehensive instructions to set up and run the Health Chatbot project, both with Docker Compose for a unified environment and using native commands for individual components.

## Table of Contents

1.  [Prerequisites](#1-prerequisites)
2.  [Project Structure](#2-project-structure)
3.  [Environment Variables](#3-environment-variables)
4.  [Running with Docker Compose (Recommended)](#4-running-with-docker-compose-recommended)
    *   [Docker Setup](#docker-setup)
    *   [Running the Services](#running-the-services)
    *   [Accessing the Application](#accessing-the-application)
    *   [Stopping Services](#stopping-services)
5.  [Running Natively (Frontend & Backend Separately)](#5-running-natively-frontend--backend-separately)
    *   [Backend Setup & Run](#backend-setup--run)
    *   [Frontend Setup & Run](#frontend-setup--run)
6.  [Seeding the Database](#6-seeding-the-database)
7.  [Test Credentials](#7-test-credentials)
8.  [Troubleshooting](#8-troubleshooting)

---

## 1. Prerequisites

Before you begin, ensure you have the following installed:

*   **Git**: For cloning the repository.
*   **Docker & Docker Compose**: (Recommended) For running the entire application in isolated containers.
*   **Python 3.9+**: For the backend (FastAPI).
*   **Node.js 18+ & npm/bun**: For the frontend (React).
*   **MongoDB**: (Required for native run) A running MongoDB instance, typically on `mongodb://localhost:27017`.
*   **Google API Key**: Required for the AI chat functionality.

## 2. Project Structure

The project consists of two main applications:

*   `healthcare-api/`: The backend FastAPI application.
*   `medicare-chat/`: The frontend React application.

```
health-chatbot/
├── healthcare-api/          # FastAPI Backend
│   ├── app/
│   ├── Dockerfile           # Dockerfile for backend
│   ├── .env.example         # Example env vars for backend
│   └── requirements.txt
├── medicare-chat/          # React Frontend
│   ├── src/
│   ├── Dockerfile           # Dockerfile for frontend
│   └── package.json
├── docker-compose.yml      # Orchestrates Docker services
├── seed-database.bat       # Windows script to seed DB
├── start-backend.bat       # Windows script to run backend natively
├── start-frontend.bat      # Windows script to run frontend natively
├── .env                    # Root .env for Docker Compose (for GOOGLE_API_KEY)
└── SETUP.md                # This guide
```

## 3. Environment Variables

Environment variables are crucial for configuring the application.

### `healthcare-api/.env` (For Native Backend Run)

Create a file named `.env` inside the `healthcare-api/` directory.

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=healthcare_db
SECRET_KEY=your-secret-key-here-change-in-production
GOOGLE_API_KEY=your_google_api_key_here
```

*   **`MONGODB_URL`**: Connection string for your MongoDB instance.
*   **`DATABASE_NAME`**: Name of the database to use.
*   **`SECRET_KEY`**: A strong, random key for JWT token signing. **Change this for production!**
*   **`GOOGLE_API_KEY`**: Your API key for Google Gemini. Obtain it from [Google AI Studio](https://aistudio.google.com/app/apikey).

### `medicare-chat/.env` (For Native Frontend Run)

Create a file named `.env` inside the `medicare-chat/` directory.

```env
VITE_API_BASE_URL=http://localhost:8000
```

*   **`VITE_API_BASE_URL`**: The base URL where the backend API is running.

### Root `.env` (For Docker Compose)

Create a file named `.env` in the **root directory** of your project (same level as `docker-compose.yml`). This is primarily to pass your `GOOGLE_API_KEY` to the backend service in Docker Compose.

```env
GOOGLE_API_KEY=your_google_api_key_here
```

## 4. Running with Docker Compose (Recommended)

This method sets up and runs both the frontend, backend, and a MongoDB instance within isolated Docker containers.

### Docker Setup

1.  **Ensure Docker is Running**: Start your Docker Desktop application or Docker daemon.
2.  **Create Root `.env`**: Make sure you have created the `.env` file in the **root directory** as described in [Environment Variables](#3-environment-variables), especially with your `GOOGLE_API_KEY`.

### Running the Services

Navigate to the **root directory** of your project in your terminal and execute:

```bash
docker-compose up -d --build
```

*   `up`: Starts the services defined in `docker-compose.yml`.
*   `-d`: Runs the containers in detached mode (in the background).
*   `--build`: Rebuilds Docker images (useful if you've made changes to Dockerfiles or dependencies).

### Accessing the Application

Once all services are up and running (this might take a few minutes for the first build):

*   **Frontend**: Open your web browser and go to [http://localhost:5173](http://localhost:5173)
*   **Backend API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Stopping Services

To stop all running Docker containers defined in `docker-compose.yml`:

```bash
docker-compose down
```

*   `down`: Stops and removes containers, networks, and volumes. Add `-v` if you want to remove the `mongo-data` volume as well, which will clear your database.

## 5. Running Natively (Frontend & Backend Separately)

This method requires Node.js, Python, and a local MongoDB instance to be installed and running on your machine.

### Backend Setup & Run (`healthcare-api/`)

1.  **Navigate to Backend**:
    ```bash
    cd healthcare-api
    ```
2.  **Create Backend `.env`**: Make sure you have created the `.env` file in this directory as described in [Environment Variables](#3-environment-variables).
3.  **Install Dependencies**:
    *   **Windows**:
        ```bash
        install-backend-deps.bat
        ```
    *   **Linux/macOS**:
        ```bash
        python -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt
        ```
        (If you prefer `uv` for dependency management: `uv venv` then `uv pip install -r requirements.txt`)
4.  **Start MongoDB**: Ensure your local MongoDB instance is running (e.g., `mongod` in a separate terminal).
5.  **Run the Backend Server**:
    *   **Windows**:
        ```bash
        start-backend.bat
        ```
    *   **Linux/macOS**:
        ```bash
        source venv/bin/activate # (if not already active)
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
        ```
    The backend will be available at [http://localhost:8000](http://localhost:8000).

### Frontend Setup & Run (`medicare-chat/`)

1.  **Navigate to Frontend**:
    ```bash
    cd medicare-chat
    ```
2.  **Create Frontend `.env`**: Make sure you have created the `.env` file in this directory as described in [Environment Variables](#3-environment-variables).
3.  **Install Dependencies**:
    *   **Windows**:
        ```bash
        npm install
        ```
    *   **Linux/macOS**:
        ```bash
        npm install # or 'bun install' if using bun
        ```
4.  **Run the Frontend Development Server**:
    *   **Windows**:
        ```bash
        start-frontend.bat
        ```
    *   **Linux/macOS**:
        ```bash
        npm run dev # or 'bun dev'
        ```
    The frontend will be available at [http://localhost:5173](http://localhost:5173).

## 6. Seeding the Database

To populate your MongoDB with sample user accounts, patient records, reports, and documents:

1.  **Ensure MongoDB is Running**: Start MongoDB (natively or via Docker Compose).
2.  **Run the Seed Script**:
    *   **Windows**: From the project's **root directory**:
        ```bash
        seed-database.bat
        ```
    *   **Linux/macOS**: From the `healthcare-api/` directory (after activating its virtual environment):
        ```bash
        python seed_database.py
        ```
    The seed script will clear existing data before adding new sample data.

## 7. Test Credentials

After seeding the database, you can use the following credentials (also found in `CREDENTIALS.md`):

*   **Test Account**:
    *   Email: `test@example.com`
    *   Password: `test123`
*   **Doctor Account**:
    *   Email: `doctor@medihelp.com`
    *   Password: `doctor123`
*   **Admin Account**:
    *   Email: `admin@medihelp.com`
    *   Password: `admin123`

## 8. Troubleshooting

*   **`GOOGLE_API_KEY not set` Error**: Ensure your `GOOGLE_API_KEY` is correctly set in the appropriate `.env` file (root `.env` for Docker, `healthcare-api/.env` for native backend).
*   **MongoDB Connection Issues**: Verify MongoDB is running and its URL is correct in your `.env` files.
*   **Frontend cannot connect to Backend**: Ensure the backend server is running and `VITE_API_BASE_URL` in `medicare-chat/.env` points to the correct backend address.
*   **Dependency Errors**: For backend, reinstall with `pip install -r requirements.txt`. For frontend, reinstall with `npm install` (or `bun install`).
*   **Pydantic UserWarnings**: "Field 'model_id' has conflict with protected namespace 'model_'". These are warnings and typically do not prevent the application from running. You can often ignore them or add `model_config['protected_namespaces'] = ()` to the `Config` class of your Pydantic models if you wish to suppress them.
