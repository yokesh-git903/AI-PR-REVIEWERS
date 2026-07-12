"""
AI Code Review Bot
-------------------
FastAPI server that listens for GitHub Pull Request webhook events,
fetches the PR diff, sends it to Claude for review, and posts the
review back as a comment on the PR.
"""

import hashlib
import hmac
import os

from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv

from app.github_utils import get_pr_diff, post_pr_comment, get_pr_files
from app.reviewer import review_code

load_dotenv()

app = FastAPI(title="AI Code Review Bot")

GITHUB_WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "")


def verify_signature(payload_body: bytes, signature_header: str) -> bool:
    """Verify that the webhook actually came from GitHub."""
    if not GITHUB_WEBHOOK_SECRET:
        # No secret configured -> skip verification (only OK for local testing)
        return True
    if not signature_header:
        return False

    hash_object = hmac.new(
        GITHUB_WEBHOOK_SECRET.encode("utf-8"), msg=payload_body, digestmod=hashlib.sha256
    )
    expected_signature = "sha256=" + hash_object.hexdigest()
    return hmac.compare_digest(expected_signature, signature_header)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "AI Code Review Bot is running 🚀"}


@app.post("/webhook")
async def github_webhook(
    request: Request,
    x_hub_signature_256: str = Header(default=None),
    x_github_event: str = Header(default=None),
):
    body = await request.body()

    if not verify_signature(body, x_hub_signature_256):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = await request.json()

    # We only care about PR opened / synchronize (new commits pushed) events
    if x_github_event != "pull_request":
        return {"message": f"Ignored event: {x_github_event}"}

    action = payload.get("action")
    if action not in ("opened", "synchronize", "reopened"):
        return {"message": f"Ignored action: {action}"}

    repo_full_name = payload["repository"]["full_name"]  # e.g. "yokesh-git903/my-repo"
    pr_number = payload["number"]

    # 1. Get the diff of the PR
    diff = get_pr_diff(repo_full_name, pr_number)

    # 2. Ask Claude to review it
    review_comment = review_code(diff)

    # 3. Post the review back as a comment on the PR
    post_pr_comment(repo_full_name, pr_number, review_comment)

    return {"message": "Review posted successfully ✅"}
