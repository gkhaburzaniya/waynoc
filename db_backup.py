from datetime import date, timedelta
from shutil import copyfile

from waynoc.local_settings import BASE_DIR, DATABASES

BACKUP_DIR = BASE_DIR.parent / ".waynoc_db_backup"
if not BACKUP_DIR.exists():
    BACKUP_DIR.mkdir()

today = date.today()

copyfile(DATABASES["default"]["NAME"], BACKUP_DIR / str(today))

for backup in BACKUP_DIR.iterdir():
    backup_date = date.fromisoformat(backup.name)

    yearly = backup_date.month == 1 and backup_date.day == 1
    monthly = backup_date.day == 1 and today - backup_date < timedelta(days=360)
    weekly = backup_date.isoweekday() == 1 and today - backup_date < timedelta(days=30)
    daily = today - backup_date < timedelta(days=7)
    if not yearly and not monthly and not weekly and not daily:
        backup.unlink()
