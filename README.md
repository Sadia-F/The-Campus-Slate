# The Campus Slate

The web platform for **The Campus Slate** — NYIT's student newspaper. A custom **Flask CMS** built to replace a paid Wix website, giving the team full control over content and cutting publishing time from days to minutes.

---

## Highlights

- 💰 Saves the team **$200+ per year** by replacing the paid Wix platform
- ⚡ Staff can self-upload articles and PDF issues via a password-protected admin dashboard
- 📰 Supports sections, staff directory, archives, and full-issue uploads
- 🌐 Deployed with Supabase (PostgreSQL) on Vercel

## Tech Stack

- **Backend:** Python, Flask 2.3
- **Database:** Supabase (PostgreSQL)
- **PDF/docs:** PyPDF2, python-docx
- **Deployment:** gunicorn + Vercel

## Getting Started

```bash
git clone https://github.com/Sadia-F/The-Campus-Slate.git
cd The-Campus-Slate
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# configure your Supabase keys/URL in the app, then:
python app.py
```

## Project Structure

```
app.py              # Flask application (routes & views)
requirements.txt    # Python dependencies
static/             # CSS, JS, images
templates/          # Jinja2 templates
  ├── home.html         # front page
  ├── sections.html     # article sections
  ├── archives.html     # past issues
  ├── upload_issue.html # upload full PDF issues
  ├── new_article.html  # write/publish articles
  ├── staff.html        # staff directory
  └── login.html        # admin auth
```

## About The Campus Slate

The Campus Slate is the official student publication of New York Institute of Technology. Built and maintained by student volunteers, it covers campus news, culture, and student life.