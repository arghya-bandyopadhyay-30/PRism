import unittest
from unittest.mock import patch, Mock

from src.utils.url_parser import parse_github_pr_url
from src.utils.constants import OWNER, REPO, PR_NUMBER


class TestParseGitHubPRUrl(unittest.TestCase):

    def setUp(self):
        patcher = patch("src.utils.url_parser.logger", new=Mock())
        self.addCleanup(patcher.stop)
        self.mock_logger = patcher.start()

    def test_valid_github_pr_url(self):
        url = "https://github.com/test-user/test-repo/pull/456"
        expected = {
            OWNER: "test-user",
            REPO: "test-repo",
            PR_NUMBER: 456
        }

        result = parse_github_pr_url(url)

        self.assertIsInstance(result, dict)
        self.assertEqual(result, expected)

    def test_invalid_github_pr_url(self):
        url = "https://github.com/invalid-url-format"
        result = parse_github_pr_url(url)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
