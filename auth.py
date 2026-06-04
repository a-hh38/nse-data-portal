import streamlit as st

USERS = {
    "athharva": "athharva123",
    "keval": "keval123",
    "vp": "vp123"
}


def login():

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.title("NSE Historical Data Portal")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if (
            username in USERS
            and USERS[username] == password
        ):

            st.session_state.authenticated = True
            st.session_state.username = username

            st.rerun()

        else:

            st.error("Invalid Username or Password")

    return False


def logout():

    if st.button("Logout"):

        st.session_state.authenticated = False

        if "username" in st.session_state:
            del st.session_state["username"]

        st.rerun()