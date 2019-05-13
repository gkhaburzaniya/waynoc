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
    if today - date.fromisoformat(backup) > timedelta(days=30):
        os.remove(os.path.join(BACKUP_DIR, backup))
