from src.api.github_api import GitHubAPIClient
from src.core.diff_parser import DiffParser


def main():
    pr_url = "https://github.com/qxresearch/qxresearch-event-1/pull/80/files"
    files = GitHubAPIClient.from_pr_url(pr_url).get_pr_files()
    parsed = DiffParser().extract_changed_lines(files)
    for line in parsed:
        print(f"{line['file_path']}-{line['line_number']}: {line['content']}")

if __name__ == "__main__":
    main()
