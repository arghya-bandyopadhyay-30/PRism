from src.api.github_api import GitHubAPIClient
from src.models.pr_file import PRFile
from src.utils.logger import PrismLogger

logger = PrismLogger.get_instance()

class GitHubService:
    def __init__(self, pr_url: str):
        self.pr_url = pr_url
        self.github_api_client = GitHubAPIClient.from_dict(self.pr_url)

    def fetch_pr_files(self) -> list[PRFile]:
        logger.info(f"Fetching PR files for {self.pr_url}")
        return self.github_api_client.get_pr_files()