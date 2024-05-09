Welcome to Henrique Schwarz Flask Web Application Template
This project serves as a template for building web applications with Flask. Below you can find links to login and detailed documentation.

Project Details
This template is designed to provide a quick start for Flask web development projects. It includes:

User Authentication
Database Integration
API Endpoints
Front-end Interaction
Webserver File Storage
First user "admin" password "admin"
Project Structure
The project is structured as follows:

            ./
            database.py
            structure.py
            app.py
            schema.sql
            routes/
                route_login.py
                route_ia.py
                route_users_adm.py
                route_dashboard.py
                route_drive.py
                __init__.py
            database/
                users.db
            uploads/
            static/
                css/
                    dashboard.css
                    drive.css
                    gerenciador_usuarios.css
                    home.css
                    login.css
                images/
                    folder-icon.png
                    file-icon.png
                js/
                    dashboard.js
                    login.js
                    home.js
            drive/
            servicos/
                service_users_adm.py
                service_ia.py
                service_drive.py
                __init__.py
            templates/
                login.html
                editar_usuario.html
                home.html
                inteligencia_artificial.html
                gerenciador_usuarios.html
                dashboard.html
                drive_index.html
                alterar_senha.html
        
Installation Requirements
Before running the application, install the required libraries:

Python, pip install database, Flask, flask_socketio, os, sqlite3, bcrypt, routes.
For more information on how to use this template and set up your own project, please visit our GitHub repository or my personal website Henrique Farisco
