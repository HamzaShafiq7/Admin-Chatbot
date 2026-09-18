import re

from database import add_user, all_users, find_user, remove_user, update_user

HELP = (
    "I can manage users for you. Try:\n"
    '- `add user "john@xyz.com" with phone number "+92332"`\n'
    '- `remove user "john@xyz.com"`\n'
    "- `update samanthas city to Cordoba`\n"
    "- `list users`"
)

FIELDS = {"name": "name", "phone": "phone", "phone number": "phone", "city": "city"}

RE_ADD = re.compile(
    r"\b(?:add|create)\s+(?:the\s+)?user\s+[\"']?([\w.\-]+@[\w.\-]+)[\"']?"
    r"(?:\s+with\s+(?:phone\s+number\s+)?[\"']?([+\d][\d\s\-]*)[\"']?)?",
    re.I,
)
RE_DEL = re.compile(
    r"\b(?:remove|delete)\s+(?:the\s+)?user\s+[\"']?([\w.\-]+@[\w.\-]+)[\"']?", re.I
)
RE_UPD = re.compile(
    r"\bupdate\s+([\w.\-]+@[\w.\-]+|\w+)\s*(?:'s)?\s+"
    r"(name|phone\s+number|phone|city)\s+to\s+(.+)",
    re.I,
)
RE_LIST = re.compile(r"\b(?:show|list|get)\s+(?:all\s+)?users\b", re.I)


def handle_command(text: str):
    m = RE_ADD.search(text)
    if m:
        email = m.group(1).lower()
        phone = (m.group(2) or "").strip()
        if find_user(email):
            return False, f"`{email}` already exists in the system."
        name = email.split("@")[0].replace(".", " ").replace("_", " ").title()
        if not add_user(email, name, phone):
            return False, f"Could not add `{email}`."
        return True, f"Added `{email}`" + (f" with phone `{phone}`." if phone else ".")

    m = RE_DEL.search(text)
    if m:
        email = m.group(1).lower()
        if remove_user(email):
            return True, f"Removed `{email}` from the system."
        return False, f"`{email}` was not found."

    m = RE_UPD.search(text)
    if m:
        ident, field = m.group(1), FIELDS[m.group(2).lower()]
        value = m.group(3).strip().strip("\"'")
        row = find_user(ident)
        if row is None:
            return False, f"No user matches `{ident}`."
        update_user(row["email"], field, value)
        return True, f"`{row['email']}` — **{field}** updated to `{value}`."

    if RE_LIST.search(text):
        rows = all_users()
        if not rows:
            return True, "No users in the system yet."
        table = "| Email | Name | Phone | City |\n|---|---|---|---|\n"
        table += "\n".join(
            f"| {r['email']} | {r['name'] or '—'} | {r['phone'] or '—'} | {r['city'] or '—'} |"
            for r in rows
        )
        return True, table
    
    return False, "Sorry, I didn't understand that.\n" + HELP