import argparse
from src.api.github_api import GitHubAPIClient
from src.core.diff_parser import DiffParser


def run(pr_url: str):
    files = GitHubAPIClient.from_pr_url(pr_url).get_pr_files()
    parsed = DiffParser().extract_changed_lines(files)
    for line in parsed:
        print(f"{line['file_path']}-{line['line_number']}: {line['content']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PRism - Pull Request Review Bot")

    parser.add_argument(
"--pr_url",
        type=str,
        required=True,
        help="GitHub pull request URL (e.g. https://github.com/user/repo/pull/123)"
    )

    args = parser.parse_args()
    run(args.pr_url)