#  Camping Fun API

A simple **Flask-based REST API** that manages campers, activities, and signups for a fictional camping program.  
This project demonstrates how to build a CRUD backend using Flask, SQLAlchemy, and Flask-Migrate.

---

##  Features

- **Campers**
  - `GET /campers` — List all campers  
  - `GET /campers/<id>` — Retrieve a camper and their signups  
  - `POST /campers` — Create a new camper (validates age 8–18)  
  - `PATCH /campers/<id>` — Update a camper’s name or age  

- **Activities**
  - `GET /activities` — List all activities  
  - `DELETE /activities/<id>` — Delete an activity (and its related signups)  

- **Signups**
  - `POST /signups` — Create a signup that links a camper to an activity at a specific time  

---

##  Tech Stack

- **Python 3.10+**
- **Flask**
- **Flask SQLAlchemy**
- **Flask Migrate**
- **SQLite** (default database)

---

##  Setup Instructions

 ### 1 Clone the repository
```bash
git clone https://github.com/yourusername/Camping-Fun-Code-Challenge.git
cd Camping-Fun-Code-Challenge

---

Create and activate a virtual environment

python -m venv env
env\Scripts\activate

Install dependencies

pip install -r requirements.txt

Initialize and migrate the database

flask db init
flask db migrate -m "Initial migration"
flask db upgrade


 Run the server

flask run --port=5555

 

Laban Mugutu
 Built with Flask, SQLAlchemy, and lots of ☕
 GITHUB: Laban Mugutu