# LodgeRover

[![Django](https://img.shields.io/badge/Django-5.2-green.svg?logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue.svg?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-24.0.9-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)


## Description
A PMS for managin reservations in hotels, touristic flats or rural homes.

## Key Features

- Two user roles: user and admin
- Create customers and reservations
- Automatically assign rooms to reservations based on the number of nights and guests
- Calculates room occupation and total prices for each reservation
- Updload documents for check in
- PayPal integration


## Prerrequisites

### 🖥️ Local

- Python 3
- PostgreSQL

## 🐳 Docker

- Docker
- Docker Compose

## Instructions to Run the Project

1. Clone this repository.
2. Navigate to the project directory.

### 🖥️ Local
1. Create vitual enviroment
  ````Shell
  python -m venv venv
  `````

2. Activate virtual enviroment
  - Windows:
````Shell
venv\Scripts\activate
`````
  - Linux/Mac:
````Shell
source venv/bin/activate
`````
3. Install dependencies
````Shell
pip install -r requirements.txt
`````
4. run server
````Shell
python manage.py runserver
`````

### 🐳 Docker
1. Build the Docker image:
  ```
  docker-compose build
  ```
2. Start the services:
  ```
  docker-compose up
  ```


### Access the application at `http://localhost:8000`.

## Images
![image](https://github.com/user-attachments/assets/5623ed9d-3bf7-476c-a54d-c37a270f044a)
![image](https://github.com/user-attachments/assets/b003c31a-e237-48cc-9fc2-fcf155a546eb)
![image](https://github.com/user-attachments/assets/9d176212-abb6-407d-a60c-ab5136f0e0e2)
![image](https://github.com/user-attachments/assets/db11f2c7-f648-4293-9ef6-e06526f83a6f)

