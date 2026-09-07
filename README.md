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
- **Frontend:** Shared responsive stylesheet (`static/css/style.css`) via a Jinja2 base layout

## Getting Started

```bash
git clone https://github.com/Sadia-F/The-Campus-Slate.git
cd The-Campus-Slate
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The app runs on `http://localhost:5002`.

### Environment Variables

Secrets are read from the environment with local fallbacks, so the app runs out of the box. Set these in your deployment (e.g. Vercel project settings) to override:

| Variable        | Description                                |
|-----------------|--------------------------------------------|
| `SUPABASE_URL`  | Supabase project URL                       |
| `SUPABASE_KEY`  | Supabase anon/public API key               |
| `TEAM_PASSWORD` | Password for the team member admin area    |
| `SECRET_KEY`    | Flask session secret                       |
| `PORT`          | Port to listen on (default `5002`)         |

## Project Structure

```
app.py              # Flask application (routes & views)
requirements.txt    # Python dependencies
static/css/style.css # shared responsive design system
templates/          # Jinja2 templates (all extend base.html)
  ├── base.html        # shared masthead, nav, footer layout
  ├── home.html        # front page
  ├── sections.html    # article sections
  ├── archives.html    # past issues
  ├── staff.html       # staff directory + team upload panel
  ├── staff_detail.html# individual staff profiles
  ├── about.html       # about the newspaper
  ├── login.html       # team member auth
  └── view_pdf.html    # full-issue PDF viewer
```

## Team Publishing Flow

1. Navigate to **Team → Login** and enter the team password.
2. On the Team page, the **Team Upload Panel** appears.
3. Upload an **Article** (title, author, date, section, content, optional image) or a **PDF Issue**.
4. New content appears immediately on the homepage; PDFs are archived under **Archives**.

## About The Campus Slate

The Campus Slate is the official student publication of New York Institute of Technology. Built and maintained by student volunteers, it covers campus news, culture, and student life.