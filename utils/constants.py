# GitHub API
GITHUB_API = "https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
STATUS_CODE_200 = 200
TIMEOUT_DEFAULT = 10

# Diff Parsing
PYTHON_FILE_EXTENSION = ".py"
PATCH_KEY = "patch"
FILENAME_KEY = "filename"
HUNK_HEADER_PREFIX = "@@"
ADDED_LINE_PREFIX = "+"
ADDED_FILE_PREFIX = "+++"
REMOVED_LINE_PREFIX = "-"
LINE_NUMBER_REGEX = r"\+(\d+)"
FILE_PATH = "file_path"
LINE_NUMBER = "line_number"
CONTENT = "content"
EMPTY_STRING = ""

# URL Parsing
GITHUB_PR_URL_PATTERN = r"https?://github\.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<pr_number>\d+)"
OWNER = "owner"
REPO = "repo"
PR_NUMBER = "pr_number"

