"""Т2: восстановление из последнего бэкапа и сверка числа записей."""
import sqlite3, glob, shutil, os

SRC = os.environ.get("EDUSYNC_DB", "edusync.db")
files = sorted(glob.glob("backups/edusync_*.db"))
if not files:
    raise SystemExit("Бэкапов нет. Сначала: python backup.py")
shutil.copy(files[-1], "edusync_restored.db")
ok = True
for t in ("users", "courses", "grades"):
    a = sqlite3.connect(SRC).execute("SELECT COUNT(*) FROM " + t).fetchone()[0]
    b = sqlite3.connect("edusync_restored.db").execute("SELECT COUNT(*) FROM " + t).fetchone()[0]
    print(t, "исходная:", a, "восстановленная:", b, "OK" if a == b else "РАСХОЖДЕНИЕ")
    ok &= (a == b)
print("РЕЗУЛЬТАТ Т2:", "ПРОЙДЕН" if ok else "НЕ ПРОЙДЕН")
