"""Автотесты: Т5 (регрессия) и Т6 (блокировка после 5 неверных паролей)."""
import os, unittest
os.environ["EDUSYNC_DB"] = "test_edusync.db"
import app


class T(unittest.TestCase):
    def setUp(self):
        if os.path.exists("test_edusync.db"):
            os.remove("test_edusync.db")
        app.DB = "test_edusync.db"
        app.init_db()
        app.register("ivan", "secret")

    def tearDown(self):
        if os.path.exists("test_edusync.db"):
            os.remove("test_edusync.db")

    def test_login_ok(self):
        self.assertTrue(app.login("ivan", "secret"))

    def test_login_wrong(self):
        self.assertFalse(app.login("ivan", "bad"))

    def test_average(self):
        c = app.add_course("Сопровождение ИС")
        app.put_grade(1, c, 5)
        app.put_grade(1, c, 4)
        self.assertEqual(app.average(1), 4.5)

    def test_lock_after_5_failures(self):
        for _ in range(5):
            app.login("ivan", "bad")
        self.assertFalse(app.login("ivan", "secret"))  # учётка заблокирована


if __name__ == "__main__":
    unittest.main(verbosity=2)
