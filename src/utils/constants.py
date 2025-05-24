GITHUB_PR_URL_PATTERN = r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<pull_number>\d+)"
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files"
OWNER = "owner"
REPO = "repo"
PR_NUMBER = "pull_number"
TIMEOUT_DEFAULT = 10
STATUS_CODE_200 = 200
