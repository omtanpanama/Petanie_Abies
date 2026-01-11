import streamlit as st
import pandas as pd

def show_admin_sidebar():
    with st.sidebar:
        st.markdown("### 🔐 Admin Panel")

        # Jika belum login
        if not st.session_state.get('logged_in', False):
            pwd = st.text_input("Password", type="password")
            if st.button("Login"):
                if pwd == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
            return None  # belum boleh akses menu

        # Jika sudah login
        else:
            menu = st.radio(
                "Menu:",
                ["📊 Dashboard Laporan"]
            )

            if st.button("Logout"):
                st.session_state.logged_in = False
                st.rerun()

            return menu


def render_dashboard():
    st.title("📊 Laporan Analisis")
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Belum ada data.")
