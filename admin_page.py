import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def show_navbar():
    with st.sidebar:
        st.markdown("### 🧭 Menu Navigasi")
        main_menu = st.selectbox("Pilih Halaman:", ["🏠 Utama", "🛡️ Admin", "👨‍🔬 Hasil Pakar"])
        
        sub_menu = None
        if main_menu == "👨‍🔬 Hasil Pakar":
            sub_menu = st.selectbox("Kategori Pakar:", ["Pakar Dosen", "Petani", "Dinas Perikanan"])
        return main_menu, sub_menu

def render_admin_login():
    st.title("🔐 Login Admin")
    if 'show_login' not in st.session_state: st.session_state.show_login = False

    if not st.session_state.get('logged_in', False):
        if not st.session_state.show_login:
            if st.button("Klik untuk Masuk Admin"):
                st.session_state.show_login = True
                st.rerun()
        else:
            pwd = st.text_input("Masukkan Sandi", type="password")
            if st.button("Login Sekarang"):
                if pwd == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
                else: st.error("Sandi Salah!")
        return False
    return True

def render_dashboard():
    st.title("📊 Laporan Google Sheets")
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0) # Ambil data terbaru
        st.dataframe(df, use_container_width=True)
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    except Exception as e: st.error(f"Gagal muat data: {e}")
