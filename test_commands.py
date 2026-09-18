import tempfile
from pathlib import Path

import database
import nlu

# Throw-away DB so the real chatbot.db stays untouched
database.DB_PATH = Path(tempfile.mkdtemp()) / "test_chatbot.db"
database.init_db()

CASES = [
    ('can you remove the user "john.smith@xyz.com"', True),
    ('can you add the user "john.smith@xyz.com" with phone number "+92332"', True),
    ("can you update samanthas city to Cordoba", True),
    ("list users", True),
    ("please do a backflip", False),
]

failures = 0
for command, expected_ok in CASES:
    ok, reply = nlu.handle_command(command)
    status = "PASS" if ok == expected_ok else "FAIL"
    failures += status == "FAIL"
    print(f"[{status}] {command!r}\n         -> {reply.splitlines()[0]}")

row = database.find_user("samantha")
assert row and row["city"] == "Cordoba", "city update did not persist!"
print("[PASS] database check: samantha.city == 'Cordoba'")

print("\nALL TESTS PASSED " if not failures else f"\n{failures} TEST(S) FAILED ")
raise SystemExit(1 if failures else 0)