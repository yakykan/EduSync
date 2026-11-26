"""EduSync: учебная мини-система (SQLite). Регистрация, вход, курсы, оценки."""
import sqlite3, hashlib, os

DB = os.environ.get("EDUSYNC_DB", "edusync.db")
MAX_ATTEMPTS = 5


def conn():
    return sqlite3.connect(DB)


def init_db():
    with conn() as c:
        c.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY, login TEXT UNIQUE, pwd_hash TEXT,
            role TEXT, failed INTEGER DEFAULT 0, locked INTEGER DEFAULT 0);
        CREATE TABLE IF NOT EXISTS courses(id INTEGER PRIMARY KEY, title TEXT);
        CREATE TABLE IF NOT EXISTS grades(
            id INTEGER PRIMARY KEY, user_id INTEGER, course_id INTEGER, grade INTEGER);
        """)


def _hash(p):
    return hashlib.sha256(("edusync:" + p).encode()).hexdigest()


def register(login, password, role="student"):
    with conn() as c:
        c.execute("INSERT INTO users(login,pwd_hash,role) VALUES(?,?,?)",
                  (login, _hash(password), role))


def login(login_, password):
    """Возвращает True при успехе. После 5 неверных попыток учётка блокируется."""
    with conn() as c:
        row = c.execute("SELECT id,pwd_hash,failed,locked FROM users WHERE login=?",
                        (login_,)).fetchone()
        if not row:
            return False
        uid, h, failed, locked = row
        if locked:
            return False
        if h == _hash(password):
            c.execute("UPDATE users SET failed=0 WHERE id=?", (uid,))
            return True
        failed += 1
        c.execute("UPDATE users SET failed=?, locked=? WHERE id=?",
                  (failed, 1 if failed >= MAX_ATTEMPTS else 0, uid))
        return False


def add_course(title):
    with conn() as c:
        return c.execute("INSERT INTO courses(title) VALUES(?)", (title,)).lastrowid


def put_grade(user_id, course_id, grade):
    with conn() as c:
        c.execute("INSERT INTO grades(user_id,course_id,grade) VALUES(?,?,?)",
                  (user_id, course_id, grade))


def average(user_id):
    with conn() as c:
        r = c.execute("SELECT AVG(grade) FROM grades WHERE user_id=?", (user_id,)).fetchone()[0]
    return round(r, 2) if r is not None else 0.0


if __name__ == "__main__":
    init_db()
    try:
        register("student1", "pass123")
        register("teacher1", "teach456", "teacher")
    except sqlite3.IntegrityError:
        pass
    print("EduSync: база готова. Вход student1:", login("student1", "pass123"))
