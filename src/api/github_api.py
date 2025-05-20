import requests
from typing import List, Dict
from src.utils.constants import GITHUB_API, STATUS_CODE_200, TIMEOUT_DEFAULT
from src.utils.logger import get_logger
from src.utils.url_parser import parse_github_pr_url

logger = get_logger(__name__)

class GitHubAPIError(Exception):
    """Custom exception for GitHub API errors."""
    pass


class GitHubAPIClient:
    """
    Client for interacting with GitHub's PR file API.
    Implements the Factory pattern via `from_pr_url`.
    """
    def __init__(self, url: str, timeout: int = TIMEOUT_DEFAULT):
        self._url = url
        self._timeout = timeout

    @classmethod
    def from_pr_url(cls, pr_url: str) -> 'GitHubAPIClient':
        pr_info = parse_github_pr_url(pr_url)
        if not pr_info:
            logger.error("Invalid GitHub PR URL.")
            raise GitHubAPIError("Invalid GitHub PR URL.")

        url = GITHUB_API.format(**pr_info)
        logger.info(f"Constructed GitHub API URL: {url}")
        return cls(url=url)

    def get_pr_files(self) -> List[Dict]:
        logger.info(f"Sending request to GitHub API...")
        try:
            response = requests.get(self._url, timeout=self._timeout)
            response.raise_for_status()
            logger.info("PR files fetched successfully.")
            return response.json() if response.status_code == STATUS_CODE_200 else []
        except requests.RequestException as exc:
            logger.exception("Error during GitHub API request.")
            raise GitHubAPIError(f"Error fetching PR files: {exc}") from exc
