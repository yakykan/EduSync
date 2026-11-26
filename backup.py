"""Т1: резервное копирование БД. Хранит последние 14 копий."""
import sqlite3, os, datetime, glob

SRC = os.environ.get("EDUSYNC_DB", "edusync.db")
DIR = "backups"
KEEP = 14


def make_backup():
    os.makedirs(DIR, exist_ok=True)
    name = os.path.join(DIR, "edusync_%s.db" % datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    src = sqlite3.connect(SRC)
    dst = sqlite3.connect(name)
    with dst:
        src.backup(dst)
    src.close(); dst.close()
    files = sorted(glob.glob(os.path.join(DIR, "edusync_*.db")))
    for old in files[:-KEEP]:
        os.remove(old)
    return name


if __name__ == "__main__":
    f = make_backup()
    print("Бэкап создан:", f, "размер:", os.path.getsize(f), "байт")
