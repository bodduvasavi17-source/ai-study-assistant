# AI Study Assistant — Hackathon Prototype

A beginner-friendly study-planning web app with a local Streamable HTTP MCP server.

## Features
- Generate a simple study plan based on subject, level, and available minutes.
- Generate beginner practice prompts.
- MCP tools: `create_study_plan` and `generate_practice_questions`.
- Runs locally without an API key.

## Important description
This is a **rule-based prototype**, not an LLM-powered chatbot. The web interface calls local Flask endpoints; the MCP endpoint exposes tools for an MCP-compatible client. Do not claim it is connected to a live Alexa+ service. For the hackathon, verify the track requirements and clearly describe the demo as a simulated experience if you choose that route.

## Requirements
- Python 3.10+
- Internet connection for first-time package installation

## Windows setup (PowerShell)
Open a terminal in this folder.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe server.py
```

If `py` is unavailable, use `python` instead. You do not need to activate the virtual environment. If your current PowerShell location is wrong, first `cd` into the folder containing `server.py`.

Open `http://127.0.0.1:5000` in your browser. The MCP endpoint is `http://127.0.0.1:8000/mcp`. Keep the terminal open while using the app; press Ctrl+C to stop.

## Troubleshooting
- `No such file`: make sure the terminal is in the folder that contains `server.py`. Run `Get-Location` and `dir`.
- `No module named flask` or `mcp`: run the pip install command above from the same project folder.
- Port in use: close the other process using port 5000 or 8000, then restart.
- PowerShell blocks activation: no activation is required; use `.venv\Scripts\python.exe` directly.

## Submission checklist
- Add a suitable open-source license (MIT is included in `LICENSE`).
- Push the project to a public GitHub repository.
- Test the app and MCP tools in an MCP-compatible client.
- Record a demo video under 3 minutes.
- Submit the repository URL, video, and required feedback on the hackathon page.
