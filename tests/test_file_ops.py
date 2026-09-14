"""Tests for file operations module."""

import tempfile
import unittest
from pathlib import Path
from src import file_ops
from src.exceptions import FileOperationError


class TestFileOps(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.test_dir.name)

    def tearDown(self):
        self.test_dir.cleanup()

    def test_write_and_read_file(self):
        test_file = self.base_path / "hello.txt"
        content = "Hello, Logging World!\nTesting file operations."
        
        chars_written = file_ops.write_file(test_file, content)
        self.assertEqual(chars_written, len(content))
        self.assertTrue(test_file.exists())

        read_content = file_ops.read_file(test_file)
        self.assertEqual(read_content, content)

    def test_read_empty_file(self):
        empty_file = self.base_path / "empty.txt"
        empty_file.touch()

        read_content = file_ops.read_file(empty_file)
        self.assertEqual(read_content, "")

    def test_read_nonexistent_file(self):
        missing_file = self.base_path / "does_not_exist.txt"
        with self.assertRaises(FileOperationError):
            file_ops.read_file(missing_file)

    def test_write_append_mode(self):
        test_file = self.base_path / "append_test.txt"
        file_ops.write_file(test_file, "Line 1\n", mode="w")
        file_ops.write_file(test_file, "Line 2\n", mode="a")

        content = file_ops.read_file(test_file)
        self.assertEqual(content, "Line 1\nLine 2\n")

    def test_write_empty_content(self):
        test_file = self.base_path / "empty_write.txt"
        chars_written = file_ops.write_file(test_file, "")
        self.assertEqual(chars_written, 0)
        self.assertTrue(test_file.exists())

    def test_write_nested_parent_dirs(self):
        nested_file = self.base_path / "subdir1" / "subdir2" / "nested.txt"
        file_ops.write_file(nested_file, "Deep file content")
        self.assertTrue(nested_file.exists())
        self.assertEqual(file_ops.read_file(nested_file), "Deep file content")


if __name__ == "__main__":
    unittest.main()
