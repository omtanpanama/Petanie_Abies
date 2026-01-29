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
            # 1. Statistik Dasar (Definisikan agar tidak NameError)
            std_dev = np.std(img_np)
            mean_val = np.mean(img_np)
            
            # 2. Cek Saturasi Warna (Screenshot/Teks biasanya warnanya flat/abu-abu)
            stat = ImageStat.Stat(img)
            # Menghitung seberapa berwarna gambar tersebut
            saturation = sum(stat.var) / len(stat.var) if hasattr(stat, 'var') else 0
            
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # --- LOGIKA FILTER SUPER KETAT ---
            # Menolak screenshot terminal (mean rendah, std tinggi)
            # Menolak kertas jurnal/diagram (mean tinggi, saturation rendah)
            is_text_or_jurnal = (mean_val > 160 and saturation < 1200) 
            is_coding_screen = (std_dev > 50 and mean_val < 100)
            is_too_flat = (std_dev < 10)
            
            if is_text_or_jurnal or is_coding_screen or is_too_flat:
                st.warning("⚠️ **Sistem mendeteksi ini bukan foto ikan asli.**")
                st.info("AI mendeteksi objek sebagai teks, jurnal, atau diagram. Pastikan foto benih ikan asli.")
                st.image(img, caption="Objek Terdeteksi Bukan Ikan", use_container_width=True)
                st.stop() # REM PAKEM: Berhenti di sini, jangan lanjut ke diagnosa
            
            # --- PROSES DIAGNOSA (Hanya jalan jika lolos filter) ---
            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"
            
            is_dry = True if mean_val > 215 else False
            gradcam_img, max_loc, heatmap_raw = generate_gradcam(img, model)
            
            st.divider()
            
            # --- TAMPILAN FOTO BERSANDINGAN (KIRI-KANAN) ---
            col_kiri, col_kanan = st.columns(2)
            with col_kiri:
                st.subheader("📸 Foto Asli")
                st.image(img, use_container_width=True)
            with col_kanan:
                st.subheader("🔥 Fokus Analisis AI")
                st.image(gradcam_img, use_container_width=True, caption=f"Area Deteksi (Akurasi: {accuracy_pct})")
            
            st.divider()

            # --- BAGIAN HASIL & PENJELASAN ---
            c_hasil, c_pakar = st.columns([1, 1.5])
            with c_hasil:
                st.write("### Hasil Diagnosa:")
                if label == "KURANG SEHAT":
                    st.error(f"## {label}")
                else:
                    st.success(f"## {label}")
                st.metric("Keyakinan AI", accuracy_pct)
            
            with c_pakar:
                st.write("### Penjelasan Pakar:")
                st.info(get_explanation(label, max_loc, heatmap_raw, is_dry))
                
            # --- SIMPAN KE DATABASE (Perbaikan NameError save_to) ---
            try:
                if "last_file" not in st.session_state or st.session_state.last_file != file.name:
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_row = pd.DataFrame([{"Waktu": waktu, "Hasil": label, "Keyakinan": accuracy_pct}])
                    save_to_google_sheets(new_row) # Pastikan nama fungsi di utils benar
                    st.session_state.last_file = file.name
            except Exception as save_err:
                st.warning(f"Data tidak tersimpan ke sheets: {save_err}")

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
