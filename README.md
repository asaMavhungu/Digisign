# Digisign

## Overview

Digisign is a digital signage system designed for dynamic content management. This project consists of a Flask-based backend that serves as the core of the system. The frontend interacts with the backend, enabling functionalities such as adding, removing, and editing content through a Flask API using REST principles.

## Getting Started

To run the Digisign project locally, follow these steps:

1. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Run the Application:**
   ```bash
   python main.py
   ```
   

## Project Structure
- main.py: The main script to initialize the Digisign backend. It includes command-line argument parsing for specifying the database type and sets up the Flask application.

- client: Module containing functionality related to the client.

- api: Module responsible for creating and configuring the Flask API.

- database: Module for creating and managing the database.
