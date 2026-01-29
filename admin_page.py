import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

def show_navbar():
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        choice = st.selectbox("Pilih Halaman:", ["🏠 Halaman Utama", "👨‍🔬 Hasil Pakar", "🛡️ Admin"])
        sub_choice = None
        if choice == "👨‍🔬 Hasil Pakar":
            sub_choice = st.selectbox("Pilih Kategori:", ["Pakar Dosen", "Petani", "Dinas Perikanan"])
        return choice, sub_choice

def render_admin_login():
    st.title("🔐 Panel Akses Admin")
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        pwd = st.text_input("Masukkan Sandi Admin", type="password")
        col1, col2 = st.columns(2)
        if col1.button("Login Sekarang"):
            if pwd == "admin123":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Sandi Salah!")
        return False
    return True

def render_dashboard():
    st.title("📊 Dashboard Laporan Analisis")
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        
        if not df.empty:
            # --- BAGIAN GRAFIK ---
            c1, c2 = st.columns([1, 1])
            with c1:
                st.write("### Ringkasan Status")
                # Grafik batang kualitas
                fig = px.bar(df['Hasil'].value_counts().reset_index(), 
                             x='Hasil', y='count', color='Hasil',
                             color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.write("### Persentase")
                # Grafik lingkaran
                fig_pie = px.pie(df, names='Hasil', hole=0.3,
                                 color='Hasil', color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig_pie, use_container_width=True)

            st.divider()
            st.dataframe(df, use_container_width=True)
            
            if st.button("Logout Admin"):
                st.session_state.logged_in = False
                st.rerun()
        else:
            st.info("Data belum tersedia di Google Sheets.")
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
