# Task Manager

Test task have been created by all the requirements.

## Installing

### 1. Clone the repo:

   ```bash
   git clone https://github.com/StanislavJPG/task_manager.git
   ```

### 2. Install requirements:
   
   ```bash
   pip install -r requirements.txt
   ```

### 3. Create your own .env file to store your secret variables:
   
   ```dotenv
   SECRET_KEY=...
   DB_NAME=...
   DB_PASS=...
   DB_USER=...
   DB_HOST=...
   DB_PORT=...
   ```

### 4. Make migrations:
   
   ```bash
   python manage.py migrate
   ```

## Running

### 1. Run your server locally:
   
   ```bash
   python manage.py runserver
   ```

### 2. Open your localhost:
   
   ```arduino
   http://127.0.0.1
   ```

### And here you go!