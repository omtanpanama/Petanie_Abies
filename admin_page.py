import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def show_navbar():
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        # Menu Utama
        choice = st.selectbox("Pilih Halaman:", ["🏠 Halaman Utama", "👨‍🔬 Hasil Pakar", "🛡️ Admin"])
        
        sub_choice = None
        if choice == "👨‍🔬 Hasil Pakar":
            sub_choice = st.selectbox("Pilih Kategori:", ["Pakar Dosen", "Petani", "Dinas Perikanan"])
            
        return choice, sub_choice

def render_admin_login():
    st.title("🔐 Panel Akses Admin")
    if 'show_login_form' not in st.session_state:
        st.session_state.show_login_form = False

    if not st.session_state.get('logged_in', False):
        if not st.session_state.show_login_form:
            if st.button("Masuk ke Sistem Admin"):
                st.session_state.show_login_form = True
                st.rerun()
        else:
            pwd = st.text_input("Masukkan Sandi Admin", type="password")
            col1, col2 = st.columns(2)
            if col1.button("Login Sekarang"):
                if pwd == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.show_login_form = False
                    st.rerun()
                else:
                    st.error("Sandi Salah!")
            if col2.button("Batal"):
                st.session_state.show_login_form = False
                st.rerun()
        return False
    return True

def render_dashboard():
    st.title("📊 Laporan Riwayat Analisis")
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            if st.button("Logout Admin"):
                st.session_state.logged_in = False
                st.rerun()
        else:
            st.info("Belum ada data di Google Sheets.")
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
