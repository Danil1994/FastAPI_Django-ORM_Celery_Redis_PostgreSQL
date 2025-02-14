# FastAPI + Django ORM + Celery + Redis + SQL

This project is a web application using **FastAPI** with **Django ORM** integration, **Celery** for 
background tasks, **Redis** as a task broker and **SQLite** as a database. The application tracks
cryptocurrency data from external sources, creates blocks with the retrieved information, and stores
them in the database.

## 📌 Features
- **FastAPI** for handling HTTP requests.
- **Django ORM** for working with the database.
- **Celery** for performing background tasks (parsing BTC and ETH blocks).
- **Redis** as a Celery task broker.
- **Docker** and **Docker Compose** for containerization of all services.

---

## 🛠 Local development (without Docker)

### 🔹 1. Clone the repository
```sh
git clone https://github.com/Danil1994/FastAPI_Django-ORM_Celery_Redis_PostgreSQL.git

```
```sh
cd to your repo
```
### 🔹 2. Create virtual env

### 🔹 3. Set up environment variables
Create a `.env` file in the root folder and specify the variables:
```env
CELERY_BROKER_URL=redis://redis:6379/0
API_KEY_BLOCKCHAIR=your_blockchair_api_key
API_KEY_COINMARKETCAP=your_coinmarketcap_api_key
```

### 🔹 4. Install dependencies
```sh
pip install -r requirements.txt
```

### 🔹 5. Install "fastapi[standard]"
```sh
pip install "fastapi[standard]"
```

### 🔹 6. Apply migrations
```sh
python manage.py makemigrations
```
```sh
python manage.py migrate
```

### 🔹 7. Run FastAPI
```sh
fastapi dev main.py
```
You may check fastapi API works here http://127.0.0.1:8000/docs

### 🔹 9. Create  superuser
```sh
 python manage.py createsuperuser
```

Admin panel availabels here http://localhost:8000/django/admin/

### 🔹 9. Run Celery
!!! Be sure that your message broker is working !!!
for example use this command in your terminal to run Redis 

docker run -d -p 6379:6379 --name redis redis

!! Be sure that docker engine is working !!

```sh
celery -A fastapi_app.celery_config worker --loglevel=info -P eventlet
```
### 🔹 10. Run Celery Beat
```sh
celery -A fastapi_app.celery_config beat --loglevel=info
```

Now app is working. Every minute it sends request to[ CoinMarketCap ](https://coinmarketcap.com/api/documentation/v1/#tag/blockchain)
and [BlockChair](https://blockchair.com/api/docs#link_002) and save data about BTC and ETH to DB.


### 🔹 Launch via Docker
```sh
docker-compose up --build
```
After that, the following will be launched:
- FastAPI application (available at `http://localhost:8000`)
- PostgreSQL (`localhost:5432`)
- Redis (`localhost:6379`)
- Celery worker

---

## 🛠 Project structure
```
fastapi_django_app/
│── fastapi_app/
│ ├── admin.py # Setup for admin panel
│ ├── app.py # FastAPI application
│ ├── celery_config.py # Celery setup
│ ├── create_fake_data.py # Create fake data for testing
│ ├── models.py # Django ORM models
│ ├── routers.py # FastAPI routers 
│ ├── schemas.py # FastAPI serializers
│ ├── tasks.py # Celery background tasks
│ ├── urls.py # Django`s urls

│── Dockerfile # Docker image for FastAPI
│── Dockerfile.celery # Docker image for Celery
│── docker-compose.yml # Docker Compose configuration
│── requirements.txt # Project dependencies
│── .env # Environment variables
```

---

## 🚀 API Endpoints
### 🔹 Registration
```http
POST /register/
```
### 🔹 Login
```http
POST /login/
```

### 🔹 Get block list
```http
GET /blocks/
```
**Filtering by currency**
```http
GET /blocks/{currency}/{block_number}
```

### 🔹 Get block details
```http
GET /blocks/{block_id}
```

### 🔹 Background task for updating blocks
Runs automatically every minute via Celery Beat.


## 📝 TODO
- [ ] Add user authentication
- [ ] Extend API endpoints
- [ ] Add tests

---

## 📜 License
MIT License. Feel free to use and modify the project! 🎉
