# Admin Chatbot 🤖

Chat-driven user management: log in with any registered email and add / remove / update users through natural-language commands.

**Stack:** Python 3 · Streamlit (chat UI + auto-login) · SQLite (zero-config)

## 📸 Preview

| Auto-Login Gate | Chat Interface & NLU |
|:---:|:---:|
| ![Login Screen](Screenshots/login.png) | ![Chat Screen](Screenshots/chat.png) |

## 🚀 Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Optional self-check (~2 s)
python test_commands.py     

# Launch the web interface
streamlit run app.py        # opens http://localhost:8501
```

## 🔐 Auto-login
Type any email that exists in the system (seeded: `admin@wpbrigade.com`,
`samantha@xyz.com`, `john.smith@xyz.com`). Unknown emails are rejected.

## ⌨️ Supported commands
| Example | Action |
|---|---|
| `can you add the user "john@xyz.com" with phone number "+92332"` | INSERT |
| `can you remove the user "john@xyz.com"` | DELETE |
| `can you update samanthas city to Cordoba` | UPDATE (name/phone/city) |
| `list users` | SHOW all |

## 📂 Project Structure
- `app.py` — Streamlit UI and session-based auto-login gate
- `nlu.py` — Natural Language Processing (Regex parser)
- `database.py` — SQLite CRUD and schema setup
- `test_commands.py` — Headless automated test suite