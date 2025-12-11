# 🌍 Travello --- Travel Booking Website

**A Full-Stack Django Web Application Containerized with Docker, Served
with Nginx, and Powered by PostgreSQL**

Travello is a fully functional travel booking website built with
**Django**, designed with a clean and modern interface, and deployed
using **Docker**, **Gunicorn**, **Nginx**, and **PostgreSQL**.\
This project demonstrates professional-level backend engineering,
containerization, and web deployment skills.

## 🚀 Features

### 🖥️ Frontend

-   Modern, responsive UI
-   Home page showcasing destinations
-   Static files served efficiently via Nginx

### 🧠 Backend (Django)

-   Django-based architecture
-   Admin panel for managing destinations and content
-   Dynamic rendering of travel destinations (name, price, description,
    image)
-   Full CRUD support in admin panel

### 🗄️ PostgreSQL Database

-   Robust, scalable relational database
-   Docker-managed database volume
-   Clean separation between app and DB

### 🐳 Dockerized Infrastructure

Everything runs in isolated containers: - **django_app** → Django +
Gunicorn backend - **postgres_db** → PostgreSQL database -
**nginx_server** → Nginx serving static files + reverse proxy

## 🧱 Project Structure

    travello-website/
    │── project/
    │── app/
    │── static/
    │── media/
    │── Dockerfile
    │── docker-compose.yml
    │── nginx/
    │     └── default.conf
    │── requirements.txt
    │── README.md

## 🐳 Running the Project With Docker

### 1️⃣ Build and start the containers

``` bash
docker-compose up --build -d
```

### 2️⃣ Apply migrations

``` bash
docker-compose exec django_app python manage.py migrate
```

### 3️⃣ Create superuser

``` bash
docker-compose exec django_app python manage.py createsuperuser
```

### 4️⃣ Access the website

-   **Frontend:** http://localhost\
-   **Admin panel:** http://localhost/admin

## 🔧 Technologies Used

  Technology   Purpose
  ------------ -------------------
  Django       Backend framework
  Gunicorn     WSGI server
  Nginx        Reverse proxy
  Docker       Containerization
  PostgreSQL   Database
  HTML/CSS     Frontend styling

## 🌟 Highlights

-   Production-ready architecture
-   Containerized for easy deployment
-   Clean and maintainable structure
-   Great for portfolio projects

## 📬 Contact

Feel free to reach out for collaboration!
