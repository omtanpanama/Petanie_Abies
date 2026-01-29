import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection

def show_navbar():
    with st.sidebar:
        st.markdown("### 🧭 Navigasi Utama")
        choice = st.selectbox("Pilih Halaman:", ["🏠 Halaman Utama", "👨‍🔬 Hasil Pakar", "🛡️ Admin"])
        sub_choice = None
        if choice == "👨‍🔬 Hasil Pakar":
            sub_choice = st.selectbox("Pilih Kategori:", ["Pakar Dosen", "Petani", "Dinas Perikanan"])
        return choice, sub_choice

def render_admin_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        st.title("🔐 Panel Akses Admin")
        with st.container(border=True):
            pwd = st.text_input("Masukkan Sandi Admin", type="password")
            if st.button("Login Sekarang", use_container_width=True):
                if pwd == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Sandi Salah!")
        return False
    return True

def render_dashboard():
    # Perbaikan: CSS dengan parameter unsafe_allow_html=True
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📊 Pusat Kendali & Analisis Data")
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        
        if not df.empty:
            # Kalkulasi
            total = len(df)
            baik = len(df[df['Hasil'] == "KUALITAS BAIK"])
            buruk = len(df[df['Hasil'] == "KURANG SEHAT"])
            sehat_rate = (baik / total) * 100 if total > 0 else 0
            
            # Akurasi Terakhir
            raw_acc = df['Keyakinan'].iloc[-1] if 'Keyakinan' in df.columns else 0
            acc_display = f"{float(raw_acc)*100:.2f}%" if isinstance(raw_acc, (float, int)) else str(raw_acc)

            # --- TAMPILAN METRIK ---
            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.container(border=True).metric("Total Scan", f"{total}")
            with m2:
                st.container(border=True).metric("Kualitas Baik", f"{baik}", f"{sehat_rate:.1f}%")
            with m3:
                st.container(border=True).metric("Kurang Sehat", f"{buruk}", delta_color="inverse")
            with m4:
                st.container(border=True).metric("Akurasi Terakhir", acc_display)

            st.divider()

            # --- GRAFIK ---
            c1, c2 = st.columns(2)
            with c1:
                fig = px.bar(df['Hasil'].value_counts().reset_index(), x='Hasil', y='count', color='Hasil',
                             color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig_pie = px.pie(df, names='Hasil', hole=0.4, color='Hasil',
                                 color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig_pie, use_container_width=True)

            if st.button("🚪 Keluar Panel Admin"):
                st.session_state.logged_in = False
                st.rerun()
        else:
            st.info("Data kosong.")
    except Exception as e:
        st.error(f"Error: {e}")
