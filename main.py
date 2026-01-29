import streamlit as st
from PIL import Image, ImageStat
from datetime import datetime
import pandas as pd
import numpy as np

from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image, save_to_google_sheets, generate_gradcam, get_explanation
from admin_page import show_navbar, render_admin_login, render_dashboard

st.set_page_config(page_title="Petani_Abies AI", layout="wide")
apply_custom_css()

try:
    model = load_model_cloud()
except Exception as e:
    st.error(f"Gagal memuat sistem: {e}")
    st.stop()

choice, sub_choice = show_navbar()
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if choice == "🏠 Halaman Utama":
    st.title("🐟 Scan Kualitas Benih Otomatis")
    file = st.file_uploader("📤 Unggah Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        img_np = np.array(img)
        
        with st.spinner("🔍 AI sedang memvalidasi objek..."):
            # 1. Hitung statistik untuk filter (PENTING!)
            std_dev = np.std(img_np)
            mean_val = np.mean(img_np)
            
            # Cek Saturasi (Screenshot/Teks biasanya warnanya flat/abu-abu)
            stat = ImageStat.Stat(img)
            saturation = sum(stat.var) / len(stat.var) # Variasi antar channel warna
            
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # 2. FILTER ANTI-SALAH (Supaya foto terminal/artikel tertolak)
            is_coding_or_text = (std_dev > 45 and mean_val < 120 and saturation < 1500)
            is_too_flat = (std_dev < 12)
            is_ambiguous = (0.49 < score < 0.51)

            if is_coding_or_text or is_too_flat or is_ambiguous:
                st.warning("⚠️ **Mohon maaf mas, ini sepertinya bukan foto ikan.**")
                st.info("AI mendeteksi ini sebagai screenshot, teks, atau gambar digital. Silakan unggah foto ikan asli.")
                st.image(img, caption="Objek Terdeteksi Bukan Ikan", use_container_width=True)
                st.stop() # PAKSA BERHENTI DI SINI
            
            # 3. PROSES DIAGNOSA (Hanya jalan jika lolos filter)
            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"
            
            is_dry = True if mean_val > 210 else False
            gradcam_img, max_loc, heatmap_raw = generate_gradcam(img, model)
            
            st.divider()
            
            # --- TAMPILAN KIRI (Foto Asli) & KANAN (Grad-CAM) ---
            col_kiri, col_kanan = st.columns(2)
            with col_kiri:
                st.subheader("📸 Foto Asli")
                st.image(img, use_container_width=True)
            with col_kanan:
                st.subheader("🔥 Fokus Analisis AI")
                st.image(gradcam_img, use_container_width=True, caption=f"Akurasi: {accuracy_pct}")
            
            st.divider()

            # --- HASIL DIAGNOSA ---
            c1, c2 = st.columns([1, 1.5])
            with c1:
                st.write("### Hasil Diagnosa:")
                if label == "KURANG SEHAT":
                    st.error(f"## {label}")
                else:
                    st.success(f"## {label}")
                st.metric("Keyakinan AI", accuracy_pct)
            with c2:
                st.write("### Penjelasan Pakar:")
                st.info(get_explanation(label, max_loc, heatmap_raw, is_dry))
                
            # Simpan otomatis
            if "last_file" not in st.session_state or st.session_state.last_file != file.name:
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{"Waktu": waktu, "Hasil": label, "Keyakinan": accuracy_pct}])
                save_to
