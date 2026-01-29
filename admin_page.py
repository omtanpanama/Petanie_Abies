import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Sistem Analisis Ikan",
    page_icon="🐟",
    layout="wide"
)

# Custom CSS untuk mempercantik UI
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    [data-testid="stMetricValue"] { font-size: 32px; font-weight: 700; color: #1e293b; }
    [data-testid="stMetricLabel"] { font-size: 16px; font-weight: 500; }
    </style>
""", unsafe_allow_index=True)

# --- 2. FUNGSI NAVIGASI ---
def show_navbar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2274/2274812.png", width=80) # Icon opsional
        st.markdown("### 🧭 Navigasi Utama")
        choice = st.selectbox("Pindah Halaman:", ["🏠 Halaman Utama", "👨‍🔬 Hasil Pakar", "🛡️ Admin"])
        
        sub_choice = None
        if choice == "👨‍🔬 Hasil Pakar":
            sub_choice = st.selectbox("Pilih Kategori:", ["Pakar Dosen", "Petani", "Dinas Perikanan"])
        
        st.divider()
        st.info("Sistem Monitoring Kualitas Ikan v1.0")
        return choice, sub_choice

# --- 3. FUNGSI LOGIN ADMIN ---
def render_admin_login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        # Judul hanya muncul di sini saat belum login
        st.title("🔐 Panel Akses Admin")
        st.markdown("Silahkan masukkan kata sandi untuk mengakses dashboard kontrol.")
        
        with st.columns([1, 2, 1])[1]: # Tengah-tengah
            with st.container(border=True):
                pwd = st.text_input("Sandi Admin", type="password")
                btn_login = st.button("Masuk Ke Dashboard", use_container_width=True)
                
                if btn_login:
                    if pwd == "admin123":
                        st.session_state.logged_in = True
                        st.success("Akses Diterima!")
                        st.rerun()
                    else:
                        st.error("Sandi salah, silahkan coba lagi.")
        return False
    return True

# --- 4. DASHBOARD UTAMA ADMIN ---
def render_dashboard():
    # Judul ini menggantikan judul login setelah berhasil masuk
    st.title("📊 Pusat Kendali & Analisis Data")
    
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        
        if not df.empty:
            # Kalkulasi Data
            total_data = len(df)
            baik = len(df[df['Hasil'] == "KUALITAS BAIK"])
            buruk = len(df[df['Hasil'] == "KURANG SEHAT"])
            sehat_rate = (baik / total_data) * 100 if total_data > 0 else 0
            
            # Ambil Akurasi Terakhir & Format ke %
            raw_acc = df['Keyakinan'].iloc[-1] if 'Keyakinan' in df.columns else 0
            try:
                acc_val = float(raw_acc) * 100
                acc_display = f"{acc_val:.2f}%"
            except:
                acc_display = str(raw_acc)

            # --- BARIS METRIK (Visual Baru) ---
            m1, m2, m3, m4 = st.columns(4)
            
            with m1:
                with st.container(border=True):
                    st.metric("Total Scan", f"{total_data} 🔍")
            
            with m2:
                with st.container(border=True):
                    st.metric("Kualitas Baik", baik, delta=f"{sehat_rate:.1f}%")
            
            with m3:
                with st.container(border=True):
                    st.metric("Kurang Sehat", buruk, delta=f"-{buruk}", delta_color="inverse")
            
            with m4:
                with st.container(border=True):
                    st.metric("Akurasi Terakhir", acc_display, delta="Model AI")

            st.markdown("### 📈 Visualisasi Data")
            c1, c2 = st.columns([1.5, 1])
            
            with c1:
                fig = px.bar(df['Hasil'].value_counts().reset_index(), 
                             x='Hasil', y='count', color='Hasil',
                             title="Distribusi Kondisi Ikan",
                             color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                fig_pie = px.pie(df, names='Hasil', hole=0.5, title="Persentase Total",
                                 color='Hasil', color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                st.plotly_chart(fig_pie, use_container_width=True)

            # --- TABEL DATA ---
            with st.expander("📑 Lihat Riwayat Data Lengkap"):
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Download Laporan (CSV)", data=csv, file_name="data_ikan.csv", mime="text/csv")

            # Tombol Keluar
            if st.button("🚪 Keluar dari Panel Admin", type="secondary"):
                st.session_state.logged_in = False
                st.rerun()

        else:
            st.warning("Data di Google Sheets masih kosong.")
            
    except Exception as e:
        st.error(f"Koneksi GSheets Gagal: {e}")

# --- 5. LOGIKA HALAMAN UTAMA ---
def main():
    choice, sub_choice = show_navbar()

    if choice == "🏠 Halaman Utama":
        st.title("🐟 Sistem Monitoring Kualitas Ikan")
        st.info("Selamat datang! Gunakan menu di samping untuk melihat hasil analisis.")
        # Bisa ditambahkan konten/hero section di sini

    elif choice == "👨‍🔬 Hasil Pakar":
        st.title(f"👨‍🔬 Analisis: {sub_choice}")
        st.write(f"Menampilkan data khusus kategori **{sub_choice}**.")
        # Filter data spesifik di sini nanti

    elif choice == "🛡️ Admin":
        if render_admin_login():
            render_dashboard()

if __name__ == "__main__":
    main()
