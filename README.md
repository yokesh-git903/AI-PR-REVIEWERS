# 🤖 AI Code Review Bot

A GitHub bot that automatically reviews Pull Requests using Claude AI.
When a PR is opened or updated, the bot fetches the diff, sends it to
Claude, and posts a structured code review as a comment on the PR.

## 🧱 Tech Stack
- **Backend:** Python (FastAPI)
- **AI:** Claude (Anthropic API)
- **Integration:** GitHub REST API + Webhooks
- **Deployment:** Render (free tier)

---

## 📁 Project Structure
```
ai-pr-reviewer/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app + webhook endpoint
│   ├── github_utils.py   # GitHub API calls (get diff, post comment)
│   └── reviewer.py        # Claude API call for reviewing code
├── requirements.txt
├── Procfile
├── .env.example
└── README.md
```

---

## 🚀 Step 1: Run it locally first

```bash
git clone <your-repo-url>
cd ai-pr-reviewer
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then fill in your real keys
uvicorn app.main:app --reload
```

Visit `http://localhost:8000` — you should see:
```json
{"status": "ok", "message": "AI Code Review Bot is running 🚀"}
```

---

## 🔑 Step 2: Get your keys

### GitHub Token
1. GitHub → Settings → Developer settings → **Personal access tokens** → Tokens (classic)
2. Generate new token → check the **repo** scope
3. Copy it into `.env` as `GITHUB_TOKEN`

### Anthropic API Key
1. Go to console.anthropic.com → API Keys → Create Key
2. Copy it into `.env` as `ANTHROPIC_API_KEY`

### Webhook Secret
Just make up any random string, e.g. `mysecret123`, put it in `.env` as `GITHUB_WEBHOOK_SECRET` — you'll use the same value in Step 4.

---

## ☁️ Step 3: Deploy to Render (free, ~5 mins)

1. Push this project to a GitHub repo.
2. Go to **render.com** → sign in with GitHub → **New +** → **Web Service**
3. Connect your repo
4. Settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add Environment Variables (same as `.env`):
   - `GITHUB_TOKEN`
   - `GITHUB_WEBHOOK_SECRET`
   - `ANTHROPIC_API_KEY`
6. Click **Deploy**. Once live, you'll get a URL like:
   `https://ai-pr-reviewer.onrender.com`

This is your **live shareable link** for the resume/HR round ✅

---

## 🔗 Step 4: Connect the webhook to your GitHub repo

1. Go to the repo you want the bot to review PRs on
2. **Settings → Webhooks → Add webhook**
3. Fill in:
   - **Payload URL:** `https://ai-pr-reviewer.onrender.com/webhook`
   - **Content type:** `application/json`
   - **Secret:** same value as `GITHUB_WEBHOOK_SECRET`
   - **Which events:** select **"Pull requests"** only
4. Save.

---

## 🧪 Step 5: Test it

1. Create a new branch, change some code, open a Pull Request against `main`
2. Within a few seconds, the bot will comment on the PR with a review like:

```
## 🤖 AI Code Review

### ✅ What's good
- Clear function naming...

### ⚠️ Issues found
- Missing null check on line 12...

### 💡 Suggestions
- Consider using a list comprehension...

### 🐛 Potential bugs
- None found
```

---
<!-- testing bot -->

