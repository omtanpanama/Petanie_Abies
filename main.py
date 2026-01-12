import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd

# Import modul lokal
from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image, save_to_google_sheets
from admin_page import show_navbar, render_admin_login, render_dashboard

# Konfigurasi Halaman
st.set_page_config(page_title="Petani_Abies AI", layout="wide")
apply_custom_css()

# Load Model (Gunakan try-except agar jika gagal download, aplikasi tidak putih/blank)
try:
    model = load_model_cloud()
except Exception as e:
    st.error(f"Gagal memuat model AI: {e}")
    st.stop()

# Tampilkan Navbar
choice, sub_choice = show_navbar()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# LOGIKA NAVIGASI
if choice == "🏠 Halaman Utama":
    st.title("🐟 Halaman Utama - Scan Ikan")
    file = st.file_uploader("📤 Upload Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        col_foto, col_aksi = st.columns([2, 1])
        with col_foto:
            st.image(img, use_container_width=True, caption="Pratinjau Foto")
        with col_aksi:
            if st.button("🔍 ANALISIS SEKARANG"):
                with st.spinner("AI sedang bekerja..."):
                    processed = preprocess_image(img)
                    prediction = model.predict(processed, verbose=0)
                    score = float(prediction[0][0])
                    waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                    
                    if score > 0.5: st.error(f"### {label}")
                    else: st.success(f"### {label}")
                    
                    new_row = pd.DataFrame([{"Waktu": waktu_sekarang, "Hasil_Klasifikasi": label, "Sigmoid_Score": score}])
                    save_to_google_sheets(new_row)
                    st.toast("Data Berhasil Dicatat!")

    st.divider()
    if not st.session_state.get('logged_in', False):
        if st.button("🔑 Login Admin Panel"):
            st.info("Beralih ke menu 'Admin' di sidebar untuk memasukkan sandi.")

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

elif choice == "👨‍🔬 Hasil Pakar":
    st.title(f"👨‍🔬 Halaman {sub_choice}")
    st.info(f"Data riwayat untuk kategori {sub_choice} dapat dilihat di sini (Sedang dikembangkan).")

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
