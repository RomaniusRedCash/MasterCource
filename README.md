# Simple JWT auth on FastAPI

## Get Started
1) ### Copy repo <br/>
```
    git clone https://github.com/aqmink/FastAPI-JWT-auth-SQLModel
```
2) ### Install requirements <br/>
create virtual enviroment
```
    python -m venv venv
```
and activate it <br/>
Windows: <br/>
```
    venv\Scripts\activate
```
Installation with pip: 
```
    pip install -r requirements.txt
```
3) ### Make migrations with Alembic <br/>
Edit alembic.ini and run
```
    alembic revision --autogenerate -m "Initial"
```
```
    alembic upgrade head
```
