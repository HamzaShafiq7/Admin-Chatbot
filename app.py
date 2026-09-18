import streamlit as st

from database import all_users, email_exists, init_db
from nlu import HELP, handle_command

st.set_page_config(page_title="Admin Chatbot", page_icon="🤖", layout="centered")
st.markdown("<style>#MainMenu, footer {visibility: hidden;}</style>", unsafe_allow_html=True)
init_db()

if "user" not in st.session_state:
    st.session_state.user = None
if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.user is None:
    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.title("Admin Chat")
        st.caption("Auto-login: enter any email that already exists in the system.")
        email = st.text_input("Email", placeholder="e.g. samantha@xyz.com")
        if st.button("Enter chat", type="primary", use_container_width=True):
            email = email.strip().lower()
            if not email:
                st.error("Please type an email address.")
            elif email_exists(email):
                st.session_state.user = email
                st.session_state.history = [
                    {"role": "assistant", "content": f"Hi **{email}** 👋\n" + HELP}
                ]
                st.rerun()
            else:
                st.error("That email isn't in the system yet — access denied.")
    st.stop()

with st.sidebar:
    st.success(f"Logged in as **{st.session_state.user}**")
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.subheader("Users in system")
    for r in all_users():
        st.caption(f"**{r['email']}**\n {r['phone'] or '—'} · {r['city'] or '—'}")
    st.divider()
    st.caption(HELP)

st.title("Admin Chatbot")
for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("e.g. update samanthas city to Cordoba"):
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    _, reply = handle_command(prompt)
    st.session_state.history.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
