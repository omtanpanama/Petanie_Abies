import streamlit as st
from PIL import Image
from datetime import datetime

# Import modul buatan sendiri
from styles import apply_custom_css, render_footer
from utils import load_model_cloud
from admin_page import show_admin_sidebar, render_admin_dashboard

# Konfigurasi
st.set_page_config(page_title="Petani_Abies AI", page_icon="🐠", layout="centered")
apply_custom_css()

# Inisialisasi State
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'history' not in st.session_state:
    st.session_state.history = []

model = load_model_cloud()

# --- SIDEBAR (DARI FILE admin_page.py) ---
admin_menu = show_admin_sidebar()

# --- LOGIKA TAMPILAN TENGAH ---
if st.session_state.get('logged_in') and admin_menu == "📊 Dashboard Laporan":
    # Tampilkan dashboard jika login dan pilih menu dashboard
    render_admin_dashboard()
else:
    # Tampilkan Halaman Scan (Halaman Utama)
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Petani_Abies AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Teknologi Cerdas untuk Kesehatan Benih Ikan Mas</p>", unsafe_allow_html=True)
    st.divider()

    uploaded_file = st.file_uploader("📤 Upload atau Ambil Foto Benih Ikan", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, use_container_width=True)
        
        if st.button("🔍 ANALISIS SEKARANG"):
            with st.spinner("AI sedang bekerja..."):
                # (Proses Model AI tetap di sini)
                label = "KUALITAS BAIK"
                st.success(f"### Hasil: {label} ✅")
                
                # Simpan history
                st.session_state.history.append({
                    "Waktu": datetime.now().strftime("%H:%M:%S"),
                    "Hasil": label
                })

render_footer()
