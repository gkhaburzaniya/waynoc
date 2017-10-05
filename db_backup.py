import os

from shutil import copyfile
from datetime import date

from waynoc.settings import BASE_DIR, DATABASES

BACKUP_DIR = os.path.join(BASE_DIR, 'db_backup')

today = date.today().toordinal()

copyfile(DATABASES['default']['NAME'], os.path.join(BACKUP_DIR, str(today)))

for backup in os.listdir(BACKUP_DIR):
    if today - int(backup) > 30:
        os.remove(os.path.join(BACKUP_DIR, backup))
