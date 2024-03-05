# Simple JWT auth on FastAPI

## Get Started
1) Copy repo <br/>
    git clone https://github.com/aqmink/FastAPI-JWT-auth-SQLModel <br/>
---
2) Install requirements <br/>
create virtual enviroment <br/>
    python -m venv venv <br/>
and activate it <br/>
Windows: <br/>
    venv\Scripts\activate <br/>
Installation with pip: <br/>
    pip install -r requirements.txt <br/>
---
3) Make migrations with Alembic <br/>
Edit alembic.ini and run <br/>
    alembic revision --autogenerate -m "Initial" <br/>
    alembic upgrade head <br/>
