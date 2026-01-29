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
        with st.container():
            pwd = st.text_input("Masukkan Sandi Admin", type="password")
            col1, col2 = st.columns([1, 1])
            if col1.button("Login Sekarang"):
                if pwd == "admin123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("Sandi Salah!")
            if col2.button("Batal"):
                st.info("Kembali ke Halaman Utama")
        return False
    return True

def render_dashboard():
    st.title("📊 Pusat Kendali & Analisis Data")
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        
        if not df.empty:
            # --- 1. RINGKASAN CEPAT (METRICS) ---
            total_data = len(df)
            baik = len(df[df['Hasil'] == "KUALITAS BAIK"])
            buruk = len(df[df['Hasil'] == "KURANG SEHAT"])
            sehat_rate = (baik / total_data) * 100 if total_data > 0 else 0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Scan", f"{total_data}")
            m2.metric("Kualitas Baik", f"{baik}", delta=f"{sehat_rate:.1f}%")
            m3.metric("Kurang Sehat", f"{buruk}", delta_color="inverse")
            m4.metric("Akurasi Terakhir", df['Keyakinan'].iloc[-1] if 'Keyakinan' in df.columns else "N/A")

            st.markdown("---")

            # --- 2. VISUALISASI GRAFIK ---
            c1, c2 = st.columns([1.2, 1])
            with c1:
                st.write("### Grafik Perbandingan")
                fig = px.bar(df['Hasil'].value_counts().reset_index(), 
                             x='Hasil', y='count', color='Hasil',
                             color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'},
                             template="plotly_white")
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.write("### Proporsi Sehat")
                fig_pie = px.pie(df, names='Hasil', hole=0.4,
                                 color='Hasil', color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig_pie, use_container_width=True)

            st.divider()

            # --- 3. TABEL DATA & EKSPOR ---
            st.subheader("📑 Riwayat Data Lengkap")
            st.dataframe(df, use_container_width=True)
            
            # Tombol Aksi di Bawah
            ca1, ca2 = st.columns([1, 1])
            with ca1:
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Ekspor ke Excel (CSV)", data=csv, file_name="laporan_ikan.csv", mime="text/csv")
            with ca2:
                if st.button("🚪 Keluar Panel Admin"):
                    st.session_state.logged_in = False
                    st.rerun()

        else:
            st.info("Data belum tersedia di Google Sheets.")
    except Exception as e:
        st.error(f"Gagal memuat dashboard: {e}")
