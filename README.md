# GEST website

## Installation and First Run on Windows PowerShell

### Requirements

Python 3.12+ installed
pip available in your terminal

### Setup

Navigate to the gesthub folder and install uv:

pip install uv -> allows creation of virtual environments
uv run manage -> creates a virtual environment on the current folder

### Database Setup

Create and apply the database migrations:

uv run manage makemigrations -> lists migrations to make
uv run manage migrate -> applies the migrations

### Run the Development Server

Start the application:

uv run manage runserver -> runs the server

The server should start locally and display the URL where the application is available (http://127.0.0.1:8000/).
To enable the gallery, another folder must be created (not currently on the repository)