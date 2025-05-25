# secret_santa_with_python

This project is a Flask application designed to organize a Secret Santa gift exchange by sending emails to participants with their assigned friend.

## Features

*   Automated random assignment of Secret Santa pairs
*   Email notifications to participants with their assigned friend

## Technologies Used

*   Python
*   Flask
*   smtplib
*   MIMEText

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yeinorvc/secret_santa_with_python.git
    cd secret_santa_with_python
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Flask development server:**
    ```bash
    flask run
    ```
2.  Open your browser and navigate to `http://127.0.0.1:5000/send-emails`.
