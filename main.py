import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd

# Import modul lokal
from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image, save_to_google_sheets
from admin_page import show_admin_sidebar, render_dashboard

# --- KONFIGURASI ---
st.set_page_config(page_title="Petani_Abies AI", layout="centered")
apply_custom_css()

# Inisialisasi State
if 'history' not in st.session_state: 
    st.session_state.history = []

# Memuat Model
model = load_model_cloud()
choice = show_admin_sidebar()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- LOGIKA NAVIGASI ---
if st.session_state.get('logged_in', False):
    # Halaman Dashboard Admin
    if choice == "📊 Dashboard Laporan":
        render_dashboard()
    elif choice == "ℹ️ Informasi Aplikasi":
        from admin_page import render_info
        render_info()
    else:
        st.info("Silakan pilih menu di sidebar")

else:
    # --- HALAMAN UTAMA (SCAN) ---
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Petani_Abies AI</h1>", unsafe_allow_html=True)
    st.divider()

    file = st.file_uploader("📤 Upload Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, use_container_width=True, caption="Pratinjau Foto")
        
        # TOMBOL ANALISIS (Hanya Satu)
        if st.button("🔍 ANALISIS SEKARANG"):
            with st.spinner("AI sedang menganalisis dan mencatat data..."):
                # 1. Pemrosesan AI
                processed = preprocess_image(img)
                prediction = model.predict(processed, verbose=0)
                score = float(prediction[0][0])  # Output Sigmoid (0-1)
                
                # 2. Penentuan Label
                label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                color = "error" if score > 0.5 else "success"
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # 3. Tampilkan Hasil di Layar
                getattr(st, color)(f"### Hasil: {label}")
                st.write(f"**AI Confidence Score (Sigmoid):** `{score:.4f}`")
                
                # 4. Simpan ke Session State (Histori Sementara)
                st.session_state.history.append({
                    "Waktu": waktu_sekarang,
                    "Hasil": label,
                    "Sigmoid_Score": round(score, 4)
                })
                
                # 5. Simpan ke Google Sheets (Data Permanen)
                new_row = pd.DataFrame([{
                    "Waktu": waktu_sekarang,
                    "Hasil_Klasifikasi": label,
                    "Sigmoid_Score": score
                }])
                
                save_to_google_sheets(new_row)
                st.toast("✅ Data berhasil dicatat ke Google Sheets!")

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
