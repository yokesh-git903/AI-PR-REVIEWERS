"""
Sends the PR diff to Google Gemini (free tier) and gets back a structured code review.
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

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

model = genai.GenerativeModel(
     model_name="gemini-flash-latest",
    system_instruction=SYSTEM_PROMPT,
)


def review_code(diff: str) -> str:
    """Send the diff to Gemini and return a formatted review comment."""
    if not diff.strip():
        return "## 🤖 AI Code Review\n\nNo changes detected to review."

    response = model.generate_content(
        f"Please review this pull request diff:\n\n```diff\n{diff}\n```"
    )

    return response.text
