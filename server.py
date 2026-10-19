"""AI Study Assistant: simple web UI + Streamable HTTP MCP server.

Run:
  python -m pip install -r requirements.txt
  python server.py

Web UI: http://127.0.0.1:5000
MCP endpoint: http://127.0.0.1:8000/mcp

This project works locally without an API key. Study plans and quizzes are
rule-based demos; no external AI model is called unless you extend the project.
"""
from __future__ import annotations

from flask import Flask, jsonify, render_template, request
from mcp.server.fastmcp import FastMCP
import threading
import webbrowser
import time

app = Flask(__name__)
mcp = FastMCP("AI Study Assistant", host="127.0.0.1", port=8000)


def make_plan(subject: str, minutes_per_day: int, level: str = "Beginner") -> dict:
    subject = (subject or "").strip()
    if not subject:
        raise ValueError("Please enter a subject.")
    if not 15 <= minutes_per_day <= 480:
        raise ValueError("Choose 15 to 480 minutes per day.")
    blocks = [
        ("Learn the core concepts", round(minutes_per_day * 0.4)),
        ("Practise with examples", round(minutes_per_day * 0.4)),
        ("Review and recall", minutes_per_day - round(minutes_per_day * 0.4) * 2),
    ]
    return {
        "subject": subject,
        "minutes_per_day": minutes_per_day,
        "level": level,
        "steps": [
            {"title": title, "minutes": mins, "detail": detail}
            for (title, mins), detail in zip(blocks, [
                f"Study one small topic in {subject}; write 3 key points.",
                f"Solve 2–5 questions or build a tiny example related to {subject}.",
                "Close your notes and explain what you learned in your own words."
            ])
        ],
        "tip": "Keep the session small. Take a short break, then mark one doubt to revisit tomorrow."
    }


def make_quiz(subject: str, count: int = 3) -> dict:
    subject = (subject or "").strip()
    if not subject:
        raise ValueError("Please enter a subject.")
    prompts = [
        f"What are the three most important beginner concepts in {subject}?",
        f"Explain one real-world use of {subject} in your own words.",
        f"What is one common mistake beginners make when learning {subject}, and how would you avoid it?",
        f"Create a small practice task that uses {subject}.",
        f"Summarize today's learning about {subject} in five sentences."
    ]
    return {"subject": subject, "questions": prompts[:max(1, min(count, len(prompts)))]}


@mcp.tool()
def create_study_plan(subject: str, minutes_per_day: int = 60, level: str = "Beginner") -> str:
    """Create a practical study plan for a subject and daily time budget."""
    try:
        result = make_plan(subject, int(minutes_per_day), level)
        return "\n".join(
            [f"Study plan: {result['subject']} ({result['level']}, {result['minutes_per_day']} min/day)"]
            + [f"{i}. {step['title']} — {step['minutes']} minutes. {step['detail']}" for i, step in enumerate(result["steps"], 1)]
            + [f"Tip: {result['tip']}"]
        )
    except (ValueError, TypeError) as exc:
        return str(exc)


@mcp.tool()
def generate_practice_questions(subject: str, count: int = 3) -> str:
    """Generate beginner-friendly practice prompts for a subject."""
    try:
        quiz = make_quiz(subject, count)
        return "\n".join([f"Practice questions for {quiz['subject']}:"] + [f"{i}. {q}" for i, q in enumerate(quiz["questions"], 1)])
    except ValueError as exc:
        return str(exc)


@app.get("/")
def index():
    return render_template("index.html")


@app.post("/api/plan")
def api_plan():
    data = request.get_json(silent=True) or {}
    try:
        result = make_plan(data.get("subject", ""), int(data.get("minutes", 60)), data.get("level", "Beginner"))
        return jsonify(result)
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


@app.post("/api/quiz")
def api_quiz():
    data = request.get_json(silent=True) or {}
    try:
        result = make_quiz(data.get("subject", ""), int(data.get("count", 3)))
        return jsonify(result)
    except (ValueError, TypeError) as exc:
        return jsonify({"error": str(exc)}), 400


def run_web():
    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    # Run the MCP endpoint in a background thread and the web app in the foreground.
    threading.Thread(target=lambda: mcp.run(transport="streamable-http"), daemon=True).start()
    time.sleep(1)
    print("\nAI Study Assistant is starting.")
    print("Web app:      http://127.0.0.1:5000")
    print("MCP endpoint: http://127.0.0.1:8000/mcp")
    print("Press Ctrl+C to stop.\n")
    run_web()
