import requests

from src.error.github_api_error import GitHubAPIError
from src.models.pr_file import PRFile
from src.utils.constants import GITHUB_API, TIMEOUT_DEFAULT, STATUS_CODE_200
from src.utils.logger import PrismLogger
from src.utils.url_parser import parse_github_pr_url

logger = PrismLogger.get_instance()

class GitHubAPIClient:
    def __init__(self, url: str, timeout: int = TIMEOUT_DEFAULT):
        self._url = url
        self._timeout = timeout

    @classmethod
    def from_dict(cls, pr_url: str) -> "GitHubAPIClient":
        pr_info = parse_github_pr_url(pr_url)
        if not pr_info:
            logger.error(f"Invalid GitHub PR URL: {pr_url}")
            raise GitHubAPIError(f"Invalid GitHub PR URL: {pr_url}")

        url = GITHUB_API.format(**pr_info)
        logger.info(f"Creating GitHub API client for {url}")
        return cls(url=url)

    def get_pr_files(self) -> list[PRFile]:
        logger.info("Sending request to GitHub API...")

        try:
            response = requests.get(self._url, timeout=self._timeout)
            response.raise_for_status()
            logger.info("PR files fetched successfully.")

            raw_files = response.json() if response.status_code == STATUS_CODE_200 else []
            return [PRFile.from_dict(f) for f in raw_files]
        except requests.RequestException as exc:
            logger.exception("Error during GitHub API request.")
            raise GitHubAPIError(f"Error fetching PR files: {exc}")

