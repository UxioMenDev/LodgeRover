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


## 🌥️ Supported Cloud Providers

### AWS S3
- **Service**: Amazon S3
- **Bucket**
- **Features**: Standard S3 storage

### Azure Blob Storage
- **Service**: Azure Blob Storage
- **Features**: SAS tokens for secure access

## 🔐 Security

### AWS S3
- Uses bucket policies for access control
- Public read access for media files
- IAM roles for secure access

### Azure Blob Storage
- Uses SAS tokens for secure access
- **No public access required**
- Time-limited URLs (1 hour default)
- Automatic token regeneration


## ⚙️ Environment Variables

Create a `.env` file in the project root with the following configuration:

```env

# Django Configuration
SECRET_KEY=your_secret_key_here


# PostgreSQL Database
POSTGRES_DB=reservation
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432

STORAGE_PROVIDER='azure' or 'aws'

# For Azure Blob Storage:
AZURE_ACCOUNT_NAME=your_azure_account
AZURE_ACCOUNT_KEY=your_azure_key
AZURE_CONTAINER=media

# For AWS S3:
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=your_region


# Unsplash API (for room images)
# Get your Access Key at: https://unsplash.com/developers
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here

```


## Images
![image](https://github.com/user-attachments/assets/5623ed9d-3bf7-476c-a54d-c37a270f044a)
<img width="1760" height="729" alt="image" src="https://github.com/user-attachments/assets/f8aaefec-3d9a-4870-ae79-9c6d89532fe8" />

<img width="3671" height="1457" alt="image" src="https://github.com/user-attachments/assets/24eee591-044f-471a-ac96-26bf4d45ca24" />


![image](https://github.com/user-attachments/assets/db11f2c7-f648-4293-9ef6-e06526f83a6f)

