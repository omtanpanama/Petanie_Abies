import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd

from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image, save_to_google_sheets, generate_gradcam, get_explanation
from admin_page import show_navbar, render_admin_login, render_dashboard

st.set_page_config(page_title="Petani_Abies AI", layout="wide")
apply_custom_css()

try:
    model = load_model_cloud()
except Exception as e:
    st.error(f"Gagal memuat model: {e}")
    st.stop()

choice, sub_choice = show_navbar()
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if choice == "🏠 Halaman Utama":
    st.title("🐟 Scan Otomatis Kualitas Ikan")
    file = st.file_uploader("📤 Upload Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    # JALANKAN OTOMATIS JIKA ADA FILE
    if file:
        img = Image.open(file).convert("RGB")
        
        with st.spinner("🔍 AI sedang menganalisis secara otomatis..."):
            # 1. Proses Prediksi
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # 2. Hitung Label & Akurasi
            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"
            
            # 3. Grad-CAM
            gradcam_img, max_loc = generate_gradcam(img, model)
            
            # TAMPILAN HASIL (Foto asli langsung diganti Grad-CAM)
            st.divider()
            col_img, col_txt = st.columns([1.2, 1])
            
            with col_img:
                st.image(gradcam_img, use_container_width=True, caption=f"Hasil Analisis Grad-CAM (Akurasi: {accuracy_pct})")
                
            with col_txt:
                if label == "KURANG SEHAT":
                    st.error(f"### HASIL: {label}")
                else:
                    st.success(f"### HASIL: {label}")
                
                st.metric("Tingkat Keyakinan AI", accuracy_pct)
                st.info(get_explanation(label, max_loc))
                
            # 4. Simpan Data (Cek session agar tidak double save saat refresh)
            if "last_processed" not in st.session_state or st.session_state.last_processed != file.name:
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{"Waktu": waktu, "Hasil": label, "Akurasi": accuracy_pct}])
                save_to_google_sheets(new_row)
                st.session_state.last_processed = file.name
                st.toast("Data otomatis tersimpan!")

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
