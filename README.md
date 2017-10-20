# Installation Instructions

With python3.6
1. `pip install -r requirements.txt`
2. `./manage.py migrate`
3. `./manage.py createsuperuser`
4. `mkdir db_backup` If you want to use the `db_backup.py` script

# Testing Instructions
1. Get geckodriver and put it in your path
2. `./manage.py test`
