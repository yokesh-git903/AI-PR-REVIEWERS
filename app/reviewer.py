"""
Sends the PR diff to Claude and gets back a structured code review.
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

SYSTEM_PROMPT = """You are an experienced senior software engineer performing a
pull request code review. Review the given git diff and provide feedback in
this exact markdown format:

## 🤖 AI Code Review

### ✅ What's good
- (bullet points)

### ⚠️ Issues found
- (bullet points, mention the file/line if visible in the diff)

### 💡 Suggestions
- (bullet points with concrete improvements)

### 🐛 Potential bugs
- (bullet points, or write "None found" if none)

Be concise, specific, and constructive. Do not repeat the whole diff back."""


def review_code(diff: str) -> str:
    """Send the diff to Claude and return a formatted review comment."""
    if not diff.strip():
        return "## 🤖 AI Code Review\n\nNo changes detected to review."

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please review this pull request diff:\n\n```diff\n{diff}\n```",
            }
        ],
    )

    review_text = "".join(
        block.text for block in message.content if block.type == "text"
    )
    return review_text
