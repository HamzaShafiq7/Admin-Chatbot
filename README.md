# Admin Chatbot 🤖

Chat-driven user management: log in with any registered email and
add / remove / update users through natural-language commands.

**Stack:** Python 3 · Streamlit (chat UI + auto-login) · SQLite (zero-config)

## Setup
```bash
pip install -r requirements.txt
python test_commands.py     # optional self-check (~2 s)
streamlit run app.py        # opens http://localhost:8501
```

## Auto-login
Type any email that exists in the system (seeded: `admin@wpbrigade.com`,
`samantha@xyz.com`, `john.smith@xyz.com`). Unknown emails are rejected.

## Supported commands
| Example | Action |
|---|---|
| `can you add the user "john@xyz.com" with phone number "+92332"` | INSERT |
| `can you remove the user "john@xyz.com"` | DELETE |
| `can you update samanthas city to Cordoba` | UPDATE (name/phone/city) |
| `list users` | SHOW all |