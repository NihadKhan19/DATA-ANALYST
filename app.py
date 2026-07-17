"""
Nihad's portfolio — Flask version.

Run with:
    pip install -r requirements.txt
    python app.py

Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)

# ============================================================
# CONTENT — edit these to update the site. Everything below
# (Jinja template + JS) reads from this data, nothing is
# hard-coded twice.
# ============================================================

PROFILE = {
    "name": "Nihad",
    "role": "Data Analyst Intern",
    "location": "India",
    "tagline": "I turn raw data into clear insights using SQL, Python and dashboards. Based in India.",
    "email": "nihadk.2026@gmailcom",
    "github": "#",
    "linkedin": "https://www.linkedin.com/in/nihad-khan/",
}

ABOUT = {
    "paragraphs": [
        "I work with data to find patterns that actually matter — cleaning messy "
        "datasets, building dashboards, and turning numbers into decisions people "
        "can act on.",
        "Currently interning as a Data Analyst, learning by working on real "
        "datasets end to end: cleaning, analysis, and reporting.",
    ],
    "facts": [
        ("Focus", "Data analysis & visualization"),
        ("Status", "Data Analyst Intern"),
        ("Experience", "Intern"),
        ("Based in", "India"),
    ],
}

# icon key maps to a small inline SVG defined in templates/index.html
PROJECTS = [
    {
        "title": "Sales Dashboard",
        "tag": "Power BI",
        "description": "Interactive dashboard tracking monthly sales and regional "
                        "performance for a retail dataset.",
        "stack": ["Power BI", "SQL"],
        "link": "#",
        "icon": "bar-chart",
    },
    {
        "title": "Customer Churn",
        "tag": "Python",
        "description": "Analysis of customer churn patterns using Python, "
                        "identifying key drop-off factors.",
        "stack": ["Python", "Pandas", "Matplotlib"],
        "link": "#",
        "icon": "trend-down",
    },
    {
        "title": "Survey Insights",
        "tag": "Excel",
        "description": "Cleaned and analyzed survey data of 2,000+ responses, "
                        "presented as a summary report.",
        "stack": ["Excel", "Statistics"],
        "link": "#",
        "icon": "clipboard",
    },
    {
        "title": "COVID Trends",
        "tag": "Visualization",
        "description": "Public health dataset explored and visualized to show "
                        "regional case trends over time.",
        "stack": ["Tableau", "SQL"],
        "link": "#",
        "icon": "activity",
    },
]

SKILLS = {
    "Languages & Analysis": [
        {"name": "SQL", "level": 85},
        {"name": "Python (Pandas)", "level": 75},
        {"name": "Excel", "level": 90},
        {"name": "Statistical Analysis", "level": 70},
    ],
    "Tools & Visualization": [
        {"name": "Power BI", "level": 80},
        {"name": "Tableau", "level": 65},
        {"name": "Jupyter Notebook", "level": 75},
        {"name": "Git", "level": 60},
    ],
}

# ============================================================
# AI ASSISTANT — simple keyword-matching FAQ bot, running fully
# in Python on the server. The front end calls POST /api/chat.
# No external API key needed. Edit KNOWLEDGE_BASE to teach it
# more answers.
# ============================================================

def _skills_list():
    return [s["name"] for group in SKILLS.values() for s in group]


def _projects_list():
    return [p["title"] for p in PROJECTS]


KNOWLEDGE_BASE = [
    {
        "keywords": ["name", "who are you", "who is nihad"],
        "answer": f"I'm {PROFILE['name']}, a {PROFILE['role']} based in "
                  f"{PROFILE['location']}, working with SQL, Python and dashboards "
                  f"to turn raw data into clear insights.",
    },
    {
        "keywords": ["skill", "tech", "stack", "tools", "know"],
        "answer": "Core skills: " + ", ".join(_skills_list()) + ".",
    },
    {
        "keywords": ["project", "work", "portfolio", "built", "made"],
        "answer": "A few projects: " + ", ".join(_projects_list())
                  + ". Scroll to the Work section to see details on each.",
    },
    {
        "keywords": ["resume", "cv", "download"],
        "answer": "You can download the resume from the Resume section — "
                  "I'll scroll you there.",
        "scrollTo": "#resume",
    },
    {
        "keywords": ["contact", "email", "reach", "hire", "linkedin", "github"],
        "answer": f"Best way to reach {PROFILE['name']} is {PROFILE['email']}, "
                  f"or check the Contact section for socials.",
        "scrollTo": "#contact",
    },
    {
        "keywords": ["experience", "background", "about", "intern"],
        "answer": "Currently interning as a Data Analyst — working on real "
                  "datasets end to end: cleaning, analysis, and reporting.",
    },
    {
        "keywords": ["hi", "hello", "hey", "sup"],
        "answer": "Hey! I'm a lightweight AI assistant for this portfolio. Ask me "
                  "about skills, projects, or how to get in touch.",
    },
]

FALLBACK = ("I don't have an answer for that yet — try asking about skills, "
            "projects, resume, or contact details.")


def get_answer(text: str) -> dict:
    lower = text.lower()
    best, best_score = None, 0
    for entry in KNOWLEDGE_BASE:
        score = sum(1 for kw in entry["keywords"] if kw in lower)
        if score > best_score:
            best_score, best = score, entry
    if best:
        return {"answer": best["answer"], "scrollTo": best.get("scrollTo")}
    return {"answer": FALLBACK, "scrollTo": None}


# ============================================================
# ROUTES
# ============================================================

@app.route("/")
def home():
    return render_template(
        "index.html",
        profile=PROFILE,
        about=ABOUT,
        projects=PROJECTS,
        skills=SKILLS,
    )


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"answer": FALLBACK, "scrollTo": None}), 400
    return jsonify(get_answer(message))


@app.route("/resume.pdf")
def resume():
    # Drop your real resume file at static/files/resume.pdf
    return send_from_directory("static/files", "CV.pdf")


if __name__ == "__main__":
    app.run(debug=True)
