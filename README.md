# Meeting to Execution Copilot

An AI-assisted workflow that turns meeting notes or transcripts into structured summaries, decisions, action items, owners and due dates. This MVP uses a local rule-based extractor so it can run without paid API credentials; an LLM integration can be added later.

## Features
- Paste meeting notes or transcript text.
- Generate a concise summary.
- Extract action items with optional owner and due date.
- Identify decision and blocker statements.
- Edit extracted tasks and download them as CSV.

## Quick start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Example input
```text
Decision: Launch the revised product page after QA approval.
Action: Priya to prepare the event tracking plan by 2026-12-05.
Blocker: Analytics access is pending from the data team.
```

## Project structure
- `app.py`: Streamlit UI and extraction logic
- `requirements.txt`: dependencies

## Limitations
The extractor relies on explicit keywords and simple patterns. It may miss implied tasks, misunderstand names or dates, and cannot infer accountability reliably. Users must review all extracted items before sharing them.

## Future improvements
- LLM-based structured extraction with JSON schema validation.
- User authentication and team workspaces.
- PostgreSQL persistence and audit history.
- Calendar/Jira integration with user approval.
- Role-based access control and retention settings.

## Author
Adarsh Kumar · [GitHub](https://github.com/adarshkumar9199)

## License
MIT
