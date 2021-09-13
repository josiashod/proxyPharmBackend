# Proxy Backend
description du projet


1. Clone the project `git clone https://github.com/josiashod/proxyPharmBackend.git`

2. Create virtual environment virtualenv env linux : `python3.8 -m venv venv` windows : `python -m venv venv`

3. Activate virtual environment linux: `source venv/bin/activate` windows: `venv\Scripts\activate.bat`

4. `pip install -r requirements.txt`

5. `python manage.py makemigrations`

6. `python manage.py migrate`

7. `python manage.py runserver`

8. To use admin create super user `python manage.py createsuperuser`

9. To save dependecies in requirements `pip freeze>requirements.txt`