import unittest
from unittest.mock import patch, Mock

from src.core.diff_parser import DiffParser
from src.utils.constants import PATCH_KEY, FILENAME_KEY


class TestDiffParser(unittest.TestCase):

    def setUp(self):
        self.parser = DiffParser()

        patcher = patch("src.core.diff_parser.logger", new=Mock())
        self.addCleanup(patcher.stop)
        self.mock_logger = patcher.start()

    def test_extract_changed_lines_from_valid_python_patch(self):
        diff_patch = (
            "@@ -0,0 +1,3 @@\n"
            "+import os\n"
            "+print('Hello')\n"
            "+# Comment line"
        )
        files_json = [{
            FILENAME_KEY: "main.py",
            PATCH_KEY: diff_patch
        }]

        result = self.parser.extract_changed_lines(files_json)

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["content"], "import os")
        self.assertEqual(result[1]["content"], "print('Hello')")
        self.assertEqual(result[2]["content"], "# Comment line")
        self.assertTrue(all(line["file_path"] == "main.py" for line in result))

    def test_skips_non_python_files(self):
        files_json = [{
            FILENAME_KEY: "README.md",
            PATCH_KEY: "@@ -1,0 +1 @@\n+This is a readme file"
        }]
        result = self.parser.extract_changed_lines(files_json)
        self.assertEqual(result, [])

    def test_skips_files_without_patch(self):
        files_json = [{
            FILENAME_KEY: "script.py"
        }]
        result = self.parser.extract_changed_lines(files_json)
        self.assertEqual(result, [])

    def test_skips_blank_or_whitespace_lines(self):
        diff_patch = (
            "@@ -1,0 +1,3 @@\n"
            "+print('Hello')\n"
            "+     \n"
            "+# Another comment"
        )
        files_json = [{
            FILENAME_KEY: "app.py",
            PATCH_KEY: diff_patch
        }]
        result = self.parser.extract_changed_lines(files_json)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["content"], "print('Hello')")
        self.assertEqual(result[1]["content"], "# Another comment")

    def test_removed_line_like_prefix_inside_addition(self):
        diff_patch = (
            "@@ -1,0 +1,2 @@\n"
            "+- print('This is not removed')\n"
            "+print('This is added')"
        )
        files_json = [{
            FILENAME_KEY: "safe.py",
            PATCH_KEY: diff_patch
        }]
        result = self.parser.extract_changed_lines(files_json)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["content"], "print('This is not removed')")
        self.assertEqual(result[1]["content"], "print('This is added')")


if __name__ == "__main__":
    unittest.main()
