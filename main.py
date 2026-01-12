import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image, save_to_google_sheets
from admin_page import show_navbar, render_admin_login, render_dashboard

st.set_page_config(page_title="Petani_Abies AI", layout="wide")
apply_custom_css()
model = load_model_cloud()

# Navigasi
choice, sub_choice = show_navbar()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

if choice == "🏠 Utama":
    st.title("🐟 Scan Kualitas Ikan")
    file = st.file_uploader("Upload Foto", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        col_foto, col_aksi = st.columns([2, 1])
        
        with col_foto:
            st.image(img, use_container_width=True, caption="Pratinjau")
            
        with col_aksi:
            # TOMBOL DI KANAN FOTO
            if st.button("🔍 ANALISIS SEKARANG"):
                with st.spinner("AI Bekerja..."):
                    # LOGIKA SCAN ASLI (TIDAK BERUBAH)
                    processed = preprocess_image(img)
                    prediction = model.predict(processed, verbose=0)
                    score = float(prediction[0][0])
                    label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                    
                    # Hasil di bawah Tombol
                    if score > 0.5: st.error(f"HASIL: {label}")
                    else: st.success(f"HASIL: {label}")
                    
                    # Simpan ke Sheets
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_data = pd.DataFrame([{"Waktu": waktu, "Hasil_Klasifikasi": label, "Sigmoid_Score": score}])
                    save_to_google_sheets(new_data)
                    st.toast("Tersimpan!")

elif choice == "🛡️ Admin":
    if render_admin_login(): render_dashboard()

elif choice == "👨‍🔬 Hasil Pakar":
    st.title(f"Halaman {sub_choice}")
    st.info(f"Konten untuk {sub_choice} akan diletakkan di sini.")

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
