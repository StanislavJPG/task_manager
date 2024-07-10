# 1. Task Manager

![capture](templates\static\img\Capture.png "Base page")

Test task have been created by all the requirements.

## Installing

### 1. Choose the right directory and clone the repo:

   ```bash
   git clone https://github.com/StanislavJPG/task_manager.git
   ```
### 2. Create venv
   ```bash
   py -m venv env
   ```

### 3. Activate venv
   ```bash
   .env\Scripts\activate
   ```
###

<details><summary>The same venv creation on Unix/Linux/macOS</summary>

### Create venv
   ```bash
   python3 -m venv env
   ```

### Activate venv
   ```bash
   source env/bin/activate
   ```
</details>

###

### 4. Choose the right manage.py project directory: 
   ```bash
   cd task_manager
   ```
###

### 5. Install the project dependencies with:
   
   ```bash
   pip install -r requirements.txt
   ```

### 6. Create your own .env file to store your secret variables:
#### Change database in settings.py if you have not postgresql database. And then also change .env

   ```dotenv
   SECRET_KEY=...
   DB_NAME=...
   DB_PASS=...
   DB_USER=...
   DB_HOST=...
   DB_PORT=...
   ```

### 7. Make migrations:
   
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
   http://127.0.0.1:8000
   ```

### And here you go!

# 2. SQL Task

<details><summary>Tasks</summary>

#### 1. get all statuses, not repeating, alphabetically ordered
```sql
SELECT DISTINCT 
    status 
FROM 
    tasks
ORDER BY 
    status ASC
```
#### 2. get the count of all tasks in each project, order by tasks count descending
```sql
SELECT 
    p.id AS project_id, 
    p.name AS project_name, 
    COUNT(t.id) AS task_count
FROM 
    projects p
JOIN 
    tasks t ON p.id = t.project_id
GROUP BY 
    p.id, p.title
ORDER BY 
    task_count DESC
```
#### 3. get the count of all tasks in each project, order by projects names
```sql
SELECT 
    p.id AS project_id, 
    p.name AS project_name, 
    COUNT(t.id) AS task_count
FROM 
    projects p
JOIN 
    tasks t ON p.id = t.project_id
GROUP BY 
    p.id, p.title
ORDER BY 
    project_name
```
#### 4. get the tasks for al projects having the name beginning with "N" letter
```sql
SELECT 
    *
FROM 
    tasks t
WHERE 
    t.name LIKE 'N%'
```
#### 5. get the list of al projects containing the 'a' letter in the 
#### middle of the name, and show the tasks count near each project. 
#### Mention that there can exist projects without tasks and tasks with project_id= NULL
```sql
SELECT
    p.name,
    COUNT(t.id) as task_count
FROM
    projects p
LEFT JOIN
    tasks t
ON p.id = t.project_id
WHERE 
    p.name LIKE '%a%'
GROUP BY p.id, p.title
```
#### 6. get the list of tasks with duplicate names. Order alphabetically
```sql
SELECT
    t.name
FROM
    tasks t
GROUP BY 
    t.name
HAVING 
    COUNT(t.name) > 1
ORDER BY 
    t.name ASC
```
#### 7. get the list of tasks having several exact matches of both name and status, from the project 'Delivery’. Order by matches count
```sql
SELECT
    t.name,
    t.status
FROM
    tasks t
INNER JOIN
    projects p
ON t.project_id = p.id
WHERE
    p.name = 'Delivery'
GROUP BY
    t.name, t.status
HAVING
    COUNT(t.status) > 1 AND COUNT(t.name) > 1
ORDER BY
    COUNT(t.name) DESC
```
#### 8. get the list of project names having more than 10 tasks in status 'completed'. Order by project_id
```sql
SELECT DISTINCT
    t.project_id,
    p.name
FROM
    projects p
INNER JOIN
    tasks t
ON p.id = t.project_id
WHERE 
    t.status = 'completed'
GROUP BY 
    t.project_id, p.name
HAVING
    COUNT(t.id) > 10
ORDER BY 
    t.project_id
	
```

</details>

###
