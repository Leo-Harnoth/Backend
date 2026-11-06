"""Unit-Tests für die Datenbank-Logik. Laufen ohne ROS:
   python3 -m unittest discover -s ros2_ws/src/assistant_backend/test -v
"""
import importlib
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


class PreferencesDbTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ["ASSISTANT_DB"] = os.path.join(self.tmp.name, "sub", "test.db")
        from assistant_backend import preferences_db
        self.db = importlib.reload(preferences_db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_default_language_for_unknown_user(self):
        self.assertEqual(self.db.get_language(42), "de")

    def test_set_and_get(self):
        self.db.set_language(1, "en")
        self.assertEqual(self.db.get_language(1), "en")

    def test_overwrite_keeps_one_row(self):
        self.db.set_language(1, "en")
        self.db.set_language(1, "de")
        self.assertEqual(self.db.get_language(1), "de")
        with self.db._connect() as c:
            self.assertEqual(c.execute("SELECT COUNT(*) FROM preferences").fetchone()[0], 1)

    def test_users_are_independent(self):
        self.db.set_language(1, "en")
        self.assertEqual(self.db.get_language(2), "de")

    def test_invalid_language_is_rejected(self):
        with self.assertRaises(ValueError):
            self.db.set_language(1, "fr")
        self.assertEqual(self.db.get_language(1), "de")

    def test_sql_injection_attempt_is_rejected(self):
        with self.assertRaises(ValueError):
            self.db.set_language(1, "en'; DROP TABLE preferences; --")
        self.assertEqual(self.db.get_language(1), "de")


if __name__ == "__main__":
    unittest.main()
