# Nihad — Portfolio (Flask / Python version)

The same portfolio, rebuilt as a Python Flask app. All content (profile,
about, projects, skills) lives in `app.py` and is rendered server-side
with Jinja templates. The "Ask my AI" chat is a real backend endpoint
(`POST /api/chat`) implemented in Python — no external API key needed,
it's a keyword-matching FAQ bot that runs on your server.

## Project structure

```
app.py                     Flask app + all content data + /api/chat endpoint
templates/
  index.html                Jinja template (renders profile/about/projects/skills)
  icons/
    bar-chart.svg            small inline icon partials used on work cards
    trend-down.svg
    clipboard.svg
    activity.svg
static/
  css/style.css              all site styling
  js/main.js                 nav scrollspy, fade-ins, skill bar animation, AI chat
  files/resume.pdf           placeholder — replace with your real resume
requirements.txt
```

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

## Editing content

Everything you'd want to change lives in `app.py`:

- `PROFILE` — name, role, tagline, email, social links
- `ABOUT` — bio paragraphs and quick facts
- `PROJECTS` — each project's title, tag, description, tech stack, link, icon
- `SKILLS` — grouped skills with proficiency percentages
- `KNOWLEDGE_BASE` — what the AI chat widget can answer

No need to touch the HTML/CSS/JS for content changes — just edit the
Python data and refresh the page.

## Real resume

Replace `static/files/resume.pdf` with your actual resume — the
Resume section's download button already points at `/resume.pdf`.

## Deploying

This needs a Python host (unlike the static HTML version), for example:
- **Render** or **Railway** — connect the repo, they auto-detect Flask
- **PythonAnywhere** — free tier works well for a small site like this
- Any VPS with `gunicorn app:app` behind nginx

Vercel/Netlify (used for the static version) don't run persistent
Python backends, so they're not a fit for this version.
