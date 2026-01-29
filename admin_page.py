import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Fish Quality Dashboard", layout="wide", page_icon="🐟")

# --- CUSTOM CSS UNTUK TAMPILAN MODERN ---
st.markdown("""
    <style>
    /* Mengubah font dan background */
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Mempercantik Card Metrik */
    [data-testid="stMetricValue"] {
        font-size: 32px;
        font-weight: 700;
        color: #1e293b;
    }
    
    /* Membuat border halus pada grafik */
    .stPlotlyChart {
        border-radius: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        background-color: white;
        padding: 10px;
    }

    /* Mempercantik Sidebar */
    .css-1d391kg {
        background-color: #ffffff;
    }

    /* Efek tombol */
    .stButton>button {
        border-radius: 8px;
        transition: all 0.3s;
        border: none;
        background-color: #3b82f6;
        color: white;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

def show_navbar():
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2271/2271068.png", width=80)
        st.markdown("## **Sistem Pakar Ikan**")
        st.divider()
        choice = st.option_menu if hasattr(st, 'option_menu') else st.selectbox(
            "📍 Navigasi Utama", 
            ["🏠 Halaman Utama", "👨‍🔬 Hasil Pakar", "🛡️ Admin"],
            index=0
        )
        
        sub_choice = None
        if choice == "👨‍🔬 Hasil Pakar":
            st.markdown("---")
            sub_choice = st.radio("🔍 Pilih Kategori:", ["Pakar Dosen", "Petani", "Dinas Perikanan"])
            
        return choice, sub_choice

def render_admin_login():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>🔐</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Panel Kontrol Admin</h3>", unsafe_allow_html=True)
        
        if 'logged_in' not in st.session_state:
            st.session_state.logged_in = False

        if not st.session_state.logged_in:
            with st.expander("Klik untuk Masuk", expanded=True):
                pwd = st.text_input("Password", type="password", placeholder="Masukkan sandi...")
                c1, c2 = st.columns(2)
                if c1.button("🚀 Masuk", use_container_width=True):
                    if pwd == "admin123":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("Sandi Salah!")
                if c2.button("🏠 Batal", use_container_width=True):
                    st.info("Kembali...")
            return False
        return True

def render_dashboard():
    # Header Section
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.title("📊 Pusat Analisis & Insight")
        st.markdown("<p style='color: #64748b;'>Memantau kualitas kesehatan ikan secara real-time</p>", unsafe_allow_html=True)
    with head_col2:
        st.write("") # Spacer
        if st.button("🚪 Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(worksheet="Sheet1", ttl=0)
        
        if not df.empty:
            # --- 1. KEY METRICS ---
            m1, m2, m3, m4 = st.columns(4)
            
            total_data = len(df)
            baik = len(df[df['Hasil'] == "KUALITAS BAIK"])
            buruk = len(df[df['Hasil'] == "KURANG SEHAT"])
            sehat_rate = (baik / total_data) * 100 if total_data > 0 else 0
            
            with m1:
                st.container()
                st.metric("Total Scan", f"{total_data} data", help="Total seluruh pemindaian")
            with m2:
                st.metric("Kondisi Baik", f"{baik}", f"{sehat_rate:.1f}%")
            with m3:
                st.metric("Kurang Sehat", f"{buruk}", f"-{(buruk/total_data*100):.1f}%", delta_color="inverse")
            with m4:
                # Ambil keyakinan terakhir jika ada
                val = df['Keyakinan'].iloc[-1] if 'Keyakinan' in df.columns else "0%"
                st.metric("Confidence Score", val)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- 2. CHARTS SECTION ---
            c1, c2 = st.columns([1.5, 1])
            
            with c1:
                st.markdown("#### 📈 Tren Distribusi")
                fig = px.bar(df['Hasil'].value_counts().reset_index(), 
                             x='Hasil', y='count', color='Hasil',
                             color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'},
                             text_auto=True)
                fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20), height=350)
                st.plotly_chart(fig, use_container_width=True)
            
            with c2:
                st.markdown("#### 🍰 Persentase")
                fig_pie = px.pie(df, names='Hasil', hole=0.5,
                                 color='Hasil', color_discrete_map={'KUALITAS BAIK': '#10b981', 'KURANG SEHAT': '#ef4444'})
                fig_pie.update_layout(margin=dict(t=20, b=20, l=20, r=20), height=350)
                st.plotly_chart(fig_pie, use_container_width=True)

            # --- 3. DATA TABLE ---
            st.markdown("#### 📑 Data Log Terkini")
            with st.expander("Lihat Detail Tabel", expanded=True):
                st.dataframe(df.style.background_gradient(subset=['Keyakinan'], cmap='Greens'), use_container_width=True)
                
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Unduh Laporan (CSV)",
                    data=csv,
                    file_name="laporan_ikan_expert.csv",
                    mime="text/csv",
                )

        else:
            st.warning("Database kosong. Belum ada data untuk dianalisis.")
    except Exception as e:
        st.error(f"Koneksi GSheets Bermasalah: {e}")

# --- LOGIC JALANNYA APLIKASI ---
page, sub_page = show_navbar()

if page == "🏠 Halaman Utama":
    st.title("Welcome to Fish Expert 🐟")
    st.info("Silakan pilih menu di samping untuk memulai.")

elif page == "👨‍🔬 Hasil Pakar":
    st.title(f"Hasil Analisis: {sub_page}")
    st.write("Konten hasil pakar akan muncul di sini...")

elif page == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()
