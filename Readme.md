


## How to use


1. Clone repository.
2. Create a virtual env.

```
    python -m venv project_env
    
    project_env\Scripts\activate.bat
```
4. Install requirements.

```
    pip install -r requirements.txt
```
5. Setup database:
```
    python manage.py makemigrations
    
    python manage.py migrate
```
6. Run server
```
    python manage.py runserver
```
7. Go to http://127.0.0.1:8000/load_data/ to prepare nutrients and foods database.


## API Reference

#### CSRF Token
For every request that requires a CSRF Token, they are provided in that page's cookies.
You need to include CSRF Token in the http header.

#### Routes
Go to http://127.0.0.1:8000/ to see all routes available.

