import re
from typing import Optional, Dict

from utils.constants import GITHUB_PR_URL_PATTERN, OWNER, REPO, PR_NUMBER
from utils.logger import get_logger

logger = get_logger(__name__)

def parse_github_pr_url(url: str) -> Optional[Dict[str, str]]:
    """
    Extracts owner, repo, and PR number from a GitHub PR URL.
    """
    match = re.match(GITHUB_PR_URL_PATTERN, url)

    if match:
        pr_info = {
            OWNER: match.group(OWNER),
            REPO: match.group(REPO),
            PR_NUMBER: int(match.group(PR_NUMBER)),
        }
        logger.info(f"Parsed GitHub PR URL: {pr_info}")
        return pr_info

    logger.error(f"Failed to parse GitHub PR URL: {url}")
    return None
