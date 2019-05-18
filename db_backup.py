import os

from shutil import copyfile
from datetime import date, timedelta

from waynoc.settings import BASE_DIR, DATABASES

BACKUP_DIR = os.path.join(BASE_DIR, '..', '.waynoc_db_backup')
if not os.path.exists(BACKUP_DIR):
    os.mkdir(BACKUP_DIR)

today = date.today()

copyfile(DATABASES['default']['NAME'], os.path.join(BACKUP_DIR, str(today)))

for backup in os.listdir(BACKUP_DIR):
    backup_date = date.fromisoformat(backup)

    yearly = backup_date.month == 1 and backup_date.day == 1
    monthly = backup_date.day == 1 and backup_date.year == today.year
    weekly = (backup_date.isoweekday() == 1
              and today - backup_date < timedelta(days=30))
    daily = today - backup_date < timedelta(days=7)
    if not yearly and not monthly and not weekly and not daily:
        os.remove(os.path.join(BACKUP_DIR, backup))
