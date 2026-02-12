import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
import numpy as np

# Import modul pendukung
from styles import apply_custom_css, render_footer
from utils import (
    load_model_cloud, preprocess_image, save_to_google_sheets, 
    generate_gradcam, get_explanation 
)
from admin_page import show_navbar, render_admin_login, render_dashboard
from hasil_pakar_dosen import render_pakar_dosen
from catatan_petani import render_catatan_petani

# 1. Konfigurasi Awal
st.set_page_config(page_title="Petani_Abies AI", layout="wide", page_icon="🐟")

apply_custom_css()

@st.cache_resource 
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

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# --- LOGIKA NAVIGASI HALAMAN ---

if choice == "🏠 Halaman Utama":
    st.title("🐟 Scan Kualitas Benih Otomatis")
    
    # --- BAGIAN INPUT NAMA PETANI (DI ATAS UPLOAD) ---
    st.markdown("### 📝 Identitas Pemilik")
    if "nama_petani" not in st.session_state:
        st.session_state.nama_petani = "" # Biarkan kosong agar user wajib isi
    
    # Input Nama Petani berada tepat sebelum uploader
    st.session_state.nama_petani = st.text_input(
        "Masukkan Nama Petani / Lokasi Sawah:", 
        value=st.session_state.nama_petani,
        placeholder="Contoh: Pak Subur - Karanggeneng"
    )
    
    # Memberi peringatan jika nama belum diisi
    if not st.session_state.nama_petani:
        st.warning("⚠️ Mohon isi nama petani terlebih dahulu sebelum mengunggah gambar.")
    
    # Tombol Upload
    file = st.file_uploader("📤 Unggah Foto Ikan", type=['jpg', 'jpeg', 'png'], disabled=not st.session_state.nama_petani)
    
    if file and st.session_state.nama_petani:
        img = Image.open(file).convert("RGB")
        img_np = np.array(img)
        
        with st.spinner(f"🔍 memindai ikan milik {st.session_state.nama_petani}..."):
            # A. Prediksi Model
            mean_val = np.mean(img_np)
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # B. Klasifikasi
            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"
            is_dry = True if mean_val > 200 else False
            
            # C. Visualisasi Grad-CAM
            gradcam_img, heatmap_raw = generate_gradcam(img, model)
            
            st.divider()
            
            # D. Tata Letak Hasil
            col_img, col_txt = st.columns([1.3, 1])
            with col_img:
                st.image(gradcam_img, use_container_width=True, 
                         caption=f"Hasil Analisis - Pemilik: {st.session_state.nama_petani}")
                
            with col_txt:
                st.markdown("### 🔍 **Hasil Analisis Kualitas AI**")
                if label == "KURANG SEHAT":
                    st.error(f"## {label}")
                else:
                    st.success(f"## {label}")
                
                st.metric("Tingkat Akurasi", accuracy_pct)
                
                explanation = get_explanation(label, heatmap_raw, is_dry)
                st.markdown("**Detail Temuan:**")
                st.info(explanation)
            
            # E. Penyimpanan Data
            if "last_processed_file" not in st.session_state or st.session_state.last_processed_file != file.name:
                try:
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_row = pd.DataFrame([{
                        "Waktu": waktu, 
                        "Petani": st.session_state.nama_petani, 
                        "Hasil": label, 
                        "Keyakinan": accuracy_pct,
                        "Detail": explanation 
                    }])
                    save_to_google_sheets(new_row)
                    st.session_state.last_processed_file = file.name
                    st.toast(f"✅ Data {st.session_state.nama_petani} berhasil disimpan!")
                except Exception as e:
                    st.error(f"Gagal simpan log: {e}")

elif choice == "👨‍🔬 Hasil Pakar":
    if sub_choice == "Pakar Dosen":
        render_pakar_dosen() 
    elif sub_choice == "Petani":
        render_catatan_petani()

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)

render_footer()
