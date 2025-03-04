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
git clone https://github.com/Danil1994/FastAPI_Django-ORM_Celery_Redis_SQL.git

```
```sh
cd to your repo
```
### 🔹 2. Create virtual env

### 🔹 3. Set up environment variables
Create a `.env.local` file in the root folder and specify the variables for local development 
and `.env.docker` file for docker

```env.example
CELERY_BROKER_URL=redis url
API_KEY_BLOCKCHAIR=your_blockchair_api_key
API_KEY_COINMARKETCAP=your_coinmarketcap_api_key
```

### 🔹 4. Install dependencies
```sh
pip install -r requirements.txt
```

### 🔹 5.  Data base configuration
By default application configurate to work with PostgreSQL. So you should configurate connection with your data base.
Or you may use SQLite, for it go to config/setting.py 
Comment existing database and uncomment SQLite DB

            # uncomment for SQLite using
            #
            # DATABASES={
            #     "default": {
            #         "ENGINE": "django.db.backends.sqlite3",
            #         "NAME": os.path.join(PROJECT_ROOT, "db.sqlite3"),
            #     }
            # },

            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.postgresql",
                    "NAME": os.getenv("POSTGRES_DB", "postgres"),
                    "USER": os.getenv("POSTGRES_USER", "postgres"),
                    "PASSWORD": os.getenv("POSTGRES_PASSWORD", "password"),
                    "HOST": os.getenv("POSTGRES_HOST", "postgres_db"),
                    "PORT": os.getenv("POSTGRES_PORT", "5432"),
                }
            },

When DB settings are ready:

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

### OPTIONAL
You may create fake data for testing

```sh
python fastapi_app/create_fake_data.py
```

(Create 50 blocks, 10 currencies, 3 providers)

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
- FastAPI docs (`http://127.0.0.1:8000/docs#/`)
- PostgreSQL (`localhost:5432`)
- Redis (`localhost:6379`)
- Django admin (`http://localhost:8000/django/admin/`)
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
