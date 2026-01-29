import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import numpy as np

# Import modul pendukung (Pastikan file-file ini ada di folder yang sama)
from styles import apply_custom_css, render_footer
from utils import (
    load_model_cloud, preprocess_image, save_to_google_sheets, 
    generate_gradcam, get_explanation
)
from admin_page import show_navbar, render_admin_login, render_dashboard
from hasil_pakar_dosen import render_pakar_dosen
from catatan_petani import render_catatan_petani

# 1. Konfigurasi Awal (Harus di baris pertama setelah import)
st.set_page_config(page_title="Petani_Abies AI", layout="wide", page_icon="🐟")

# Menerapkan CSS Kustom
apply_custom_css()

# 2. Load Model dengan Error Handling
@st.cache_resource # Menambahkan cache agar model tidak reload setiap kali ganti halaman
def get_model():
    try:
        return load_model_cloud()
    except Exception as e:
        st.error(f"❌ Gagal memuat model AI: {e}")
        return None

model = get_model()
if model is None:
    st.stop()

# 3. Navigasi Sidebar
choice, sub_choice = show_navbar()

# Pembungkus konten utama untuk styling
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- LOGIKA NAVIGASI HALAMAN ---

if choice == "🏠 Halaman Utama":
    st.title("🐟 Scan Kualitas Benih Otomatis")
    st.write("Unggah foto benih ikan untuk mendeteksi kesehatan secara instan.")
    
    file = st.file_uploader("📤 Unggah Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        img_np = np.array(img)
        
        with st.spinner("🔍 AI sedang memindai fisik ikan..."):
            # A. Ekstraksi Fitur Dasar
            mean_val = np.mean(img_np)
            
            # B. Prediksi Model
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # C. Klasifikasi Hasil
            # Asumsi: score > 0.5 berarti Kurang Sehat, menyesuaikan dengan logika Anda
            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"
            
            # Cek Kondisi Fisik Tambahan (Pucat/Kering)
            is_dry = True if mean_val > 200 else False
            
            # D. Visualisasi Grad-CAM (Heatmap)
            gradcam_img, max_loc, heatmap_raw = generate_gradcam(img, model)
            
            st.divider()
            
            # Tata Letak Hasil Diagnosa
            col_img, col_txt = st.columns([1.3, 1])
            
            with col_img:
                st.image(gradcam_img, use_container_width=True, 
                         caption=f"Visualisasi Grad-CAM (Keyakinan: {accuracy_pct})")
                
            with col_txt:
                st.write("### 🩺 Diagnosa Pakar AI:")
                if label == "KURANG SEHAT":
                    st.error(f"## {label}")
                else:
                    st.success(f"## {label}")
                
                # Tampilan Metrik Akurasi di Halaman Utama
                st.metric("Tingkat Keyakinan AI", accuracy_pct)
                
                # Penjelasan Detail
                explanation = get_explanation(label, max_loc, heatmap_raw, is_dry)
                st.info(explanation)
            
            # E. Penyimpanan Data ke Google Sheets
            # Menggunakan session state agar tidak double save saat aplikasi rerun
            if "last_processed_file" not in st.session_state or st.session_state.last_processed_file != file.name:
                try:
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_row = pd.DataFrame([{
                        "Waktu": waktu, 
                        "Hasil": label, 
                        "Keyakinan": accuracy_pct
                    }])
                    save_to_google_sheets(new_row)
                    st.session_state.last_processed_file = file.name
                except Exception as e:
                    st.sidebar.error(f"Gagal simpan log: {e}")

elif choice == "👨‍🔬 Hasil Pakar":
    if sub_choice == "Pakar Dosen":
        render_pakar_dosen() 
    elif sub_choice == "Petani":
        render_catatan_petani()
    elif sub_choice == "Dinas Perikanan":
        st.title("🏛️ Dinas Perikanan")
        st.info("Menampilkan informasi regulasi dan standar kualitas dari Dinas Perikanan.")

elif choice == "🛡️ Admin":
    # Fungsi ini menghandle form login dan menampilkan dashboard jika sukses
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)

# 4. Footer
render_footer()
