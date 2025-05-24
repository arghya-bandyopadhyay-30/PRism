from src.models.pr_file import PRFile
from src.service.github_service import GitHubService
from src.utils.logger import PrismLogger

logger = PrismLogger.get_instance()

class GitHubController:
    def __init__(self, pr_url: str):
        self.pr_url = pr_url
        self.service = GitHubService(pr_url)

    def get_changed_files(self) -> list[PRFile]:
        logger.info("Controller invoked to get changed PR files.")
        return self.service.fetch_pr_files()

