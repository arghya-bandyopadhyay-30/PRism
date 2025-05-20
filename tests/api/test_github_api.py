import unittest
from unittest.mock import patch, Mock

from requests import RequestException

from src.api.github_api import GitHubAPIClient, GitHubAPIError
from src.utils.constants import GITHUB_API
from requests.exceptions import HTTPError


class TestGitHubAPIClient(unittest.TestCase):

    def setUp(self):
        self.valid_pr_url = "https://github.com/test-user/test-repo/pull/123"
        self.invalid_pr_url = "https://github.com/invalid-url"

        patcher = patch("src.api.github_api.logger", new=Mock())
        self.addCleanup(patcher.stop)
        self.mock_logger = patcher.start()

    def test_from_pr_url_success(self):
        client = GitHubAPIClient.from_pr_url(self.valid_pr_url)
        expected_url = GITHUB_API.format(owner="test-user", repo="test-repo", pr_number=123)
        self.assertEqual(client._url, expected_url)

    def test_from_pr_url_invalid(self):
        with self.assertRaises(GitHubAPIError) as context:
            GitHubAPIClient.from_pr_url(self.invalid_pr_url)
        self.assertIn("Invalid GitHub PR URL", str(context.exception))

    @patch("src.api.github_api.requests.get")
    def test_get_pr_files_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"filename": "file.py", "patch": "@@ -1,0 +1,2 @@\n+print('Hello')"}]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        files = GitHubAPIClient.from_pr_url(self.valid_pr_url).get_pr_files()

        self.assertIsInstance(files, list)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0]["filename"], "file.py")

    @patch("src.api.github_api.requests.get")
    def test_get_pr_files_http_error(self, mock_get):
        mock_get.side_effect = RequestException("GitHub API is down")

        client = GitHubAPIClient.from_pr_url(self.valid_pr_url)
        with self.assertRaises(GitHubAPIError) as context:
            client.get_pr_files()

        self.assertIn("Error fetching PR files", str(context.exception))

    @patch("src.api.github_api.requests.get")
    def test_get_pr_files_non_200_status(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = HTTPError("404 Not Found")
        mock_get.return_value = mock_response

        client = GitHubAPIClient.from_pr_url(self.valid_pr_url)
        with self.assertRaises(GitHubAPIError) as context:
            client.get_pr_files()

        self.assertIn("Error fetching PR files", str(context.exception))


if __name__ == "__main__":
    unittest.main()
