# Notifier Project

## Overview

The Notifier project is a Python-based application designed to send notifications via email. It includes functionality for testing email configurations and sending notifications based on specific triggers.

## Project Structure

```
notifier/
├── __pycache__/
├── .envv
├── .gitignore
├── .pytest_cache/
├── bin/
├── Dockerfile
├── email_tester.py
├── emails/
├── execute.sh
├── main.py
├── Procfile
├── pytest.ini
├── pyvenv.cfg
├── README.md
├── requirements.txt
├── src/
└── venv/
```

## Getting Started

### Prerequisites

- Python 3.x
- Docker (optional, for containerized deployment)

### Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd notifier
    ```

2. Create and activate a virtual environment:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Copy the `.env.example` file to `.env` and update the necessary configurations.

### Running the Application

To run the main application:
```sh
python main.py
```

## Docker

To build and run the application using Docker:

1. Build the Docker image:
    ```sh
    docker build -t notifier .
    ```

2. Run the Docker container:
    ```sh
    docker run -d --env-file .env notifier
    ```

## Files and Directories

- `main.py`: The main entry point of the application.
- `email_tester.py`: A script for testing email configurations.
- `emails/`: Directory containing email templates.
- `requirements.txt`: List of Python dependencies.
- `Dockerfile`: Docker configuration for containerizing the application.
- `execute.sh`: Shell script for executing specific tasks.
- `src/`: Source code directory.
- `venv/`: Virtual environment directory.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any changes.
