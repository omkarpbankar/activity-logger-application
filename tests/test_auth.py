"""Tests for authentication module."""

import unittest
from src import auth
from src.exceptions import AuthenticationError


class TestAuth(unittest.TestCase):
    def setUp(self):
        auth.reset_session()

    def tearDown(self):
        auth.reset_session()

    def test_successful_login(self):
        result = auth.login("admin", "admin123")
        self.assertTrue(result)
        self.assertTrue(auth.is_authenticated())
        self.assertEqual(auth.get_current_user(), "admin")

    def test_login_invalid_password(self):
        with self.assertRaises(AuthenticationError):
            auth.login("admin", "wrongpassword")
        self.assertFalse(auth.is_authenticated())
        self.assertIsNone(auth.get_current_user())

    def test_login_nonexistent_user(self):
        with self.assertRaises(AuthenticationError):
            auth.login("nonexistent_user", "pass")
        self.assertFalse(auth.is_authenticated())

    def test_login_empty_username(self):
        with self.assertRaises(AuthenticationError):
            auth.login("", "pass")

    def test_already_logged_in_rejection(self):
        auth.login("admin", "admin123")
        second_attempt = auth.login("alice", "secret456")
        self.assertFalse(second_attempt)
        self.assertEqual(auth.get_current_user(), "admin")

    def test_successful_logout(self):
        auth.login("alice", "secret456")
        self.assertTrue(auth.logout())
        self.assertFalse(auth.is_authenticated())
        self.assertIsNone(auth.get_current_user())

    def test_logout_without_session(self):
        self.assertFalse(auth.logout())


if __name__ == "__main__":
    unittest.main()
