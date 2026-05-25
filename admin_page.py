import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from google.oauth2.service_account import Credentials

def show_navbar():
    with st.sidebar:
        st.markdown("### 🧭 Navigasi")
        choice = st.selectbox("Pilih Halaman:", ["🏠 Halaman Utama", "👨‍🔬 Hasil Pakar", "🛡️ Admin"])
        sub_choice = None
        if choice == "👨‍🔬 Hasil Pakar":
            sub_choice = st.selectbox("Pilih Kategori:", ["Pakar Dosen", "Petani"])
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
        # MEMBACA TOML MURNI LANGSUNG DARI SECRETS (PENGGANTI BASE64)
        creds_json = dict(st.secrets["gcp_credentials"])
        
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_info(creds_json, scopes=scope)
        client = gspread.authorize(creds)
        
        spreadsheet_url = st.secrets["connections"]["gsheets"]["spreadsheet"]
        sheet = client.open_by_url(spreadsheet_url).sheet1
        
        records = sheet.get_all_records()
        df = pd.DataFrame(records)
        
        if not df.empty:
            st.markdown("### 🔍 Filter Laporan")
            if 'Petani' in df.columns:
                list_petani = ["Semua Petani"] + sorted(df['Petani'].dropna().unique().tolist())
                pilihan_petani = st.selectbox("Lihat data milik:", list_petani)
                
                if pilihan_petani != "Semua Petani":
                    df_filtered = df[df['Petani'] == pilihan_petani]
                else:
                    df_filtered = df
            else:
                df_filtered = df
                st.warning("Kolom 'Petani' tidak ditemukan di database.")

            st.divider()

            total_data = len(df_filtered)
            baik = len(df_filtered[df_filtered['Hasil'] == "KUALITAS BAIK"])
            buruk = len(df_filtered[df_filtered['Hasil'] == "KURANG SEHAT"])
            sehat_rate = (baik / total_data) * 100 if total_data > 0 else 0

            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Scan", f"{total_data}")
            m2.metric("Kualitas Baik", f"{baik}", delta=f"{sehat_rate:.1f}%")
            m3.metric("Kurang Sehat", f"{buruk}", delta_color="inverse")
            
            last_acc = df_filtered['Keyakinan'].iloc[-1] if not df_filtered.empty and 'Keyakinan' in df_filtered.columns else "N/A"
            m4.metric("Akurasi Terakhir", last_acc)

            st.markdown("---")

            if total_data > 0:
                c1, c2 = st.columns([1.2, 1])
                with c1:
                    st.write(f"### Grafik Perbandingan: {pilihan_petani}")
                    counts = df_filtered['Hasil'].value_counts().reset_index()
                    counts.columns = ['Hasil', 'count']
                    fig = px.bar(counts, x='Hasil', y='count', color='Hasil',
                                 color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'},
                                 template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
                
                with c2:
                    st.write("### Proporsi Kesehatan")
                    fig_pie = px.pie(df_filtered, names='Hasil', hole=0.4,
                                     color='Hasil', color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                    st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("Tidak ada data untuk filter ini.")

            st.divider()

            st.subheader(f"📑 Riwayat Data: {pilihan_petani}")
            st.dataframe(df_filtered, use_container_width=True)
            
            ca1, ca2 = st.columns([1, 1])
            with ca1:
                csv = df_filtered.to_csv(index=False).encode('utf-8')
                st.download_button(f"📥 Ekspor Data {pilihan_petani}", data=csv, file_name=f"laporan_{pilihan_petani}.csv", mime="text/csv")
            with ca2:
                if st.button("🚪 Keluar Panel Admin"):
                    st.session_state.logged_in = False
                    st.rerun()
        else:
            st.info("Data belum tersedia di Google Sheets.")
    except Exception as e:
        st.error(f"Gagal memuat dashboard: {e}")
