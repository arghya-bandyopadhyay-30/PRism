import argparse

from src.controller.github_controller import GitHubController


def main(pr_url: str):
    controller = GitHubController(pr_url)
    files = controller.get_changed_files()

    for f in files:
        print(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PRism - Pull Request Review Bot")
    parser.add_argument("--pr_url", type=str, required=True, help="GitHub PR URL")
    args = parser.parse_args()
    main(args.pr_url)