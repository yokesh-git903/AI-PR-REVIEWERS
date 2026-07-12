"""
Helper functions to talk to the GitHub REST API:
- fetch a PR's diff
- fetch changed files
- post a comment back on the PR
"""

import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_API_URL = "https://api.github.com"


def _headers(accept: str = "application/vnd.github+json"):
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": accept,
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_pr_diff(repo_full_name: str, pr_number: int) -> str:
    """Fetch the raw diff of a pull request."""
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/pulls/{pr_number}"
    response = requests.get(url, headers=_headers(accept="application/vnd.github.v3.diff"))
    response.raise_for_status()

    diff = response.text
    # GitHub diffs can be huge — truncate to stay within LLM context limits
    max_chars = 15000
    if len(diff) > max_chars:
        diff = diff[:max_chars] + "\n\n...[diff truncated for length]..."
    return diff


def get_pr_files(repo_full_name: str, pr_number: int):
    """Fetch list of files changed in the PR (name + status + patch)."""
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/pulls/{pr_number}/files"
    response = requests.get(url, headers=_headers())
    response.raise_for_status()
    return response.json()


def post_pr_comment(repo_full_name: str, pr_number: int, comment_body: str):
    """Post a comment on the PR's conversation tab."""
    url = f"{GITHUB_API_URL}/repos/{repo_full_name}/issues/{pr_number}/comments"
    response = requests.post(url, headers=_headers(), json={"body": comment_body})
    response.raise_for_status()
    return response.json()
