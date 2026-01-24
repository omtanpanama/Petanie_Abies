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
    st.error(f"Gagal memuat sistem: {e}")
    st.stop()

choice, sub_choice = show_navbar()
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if choice == "🏠 Halaman Utama":
    st.title("🐟 Scan Kualitas Benih Otomatis")
    file = st.file_uploader("📤 Unggah Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        
        # PROSES OTOMATIS
        with st.spinner("🔍 AI sedang memindai seluruh bagian tubuh ikan..."):
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # Keyakinan Model (Sigmoid 0-1)
            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"
            
            gradcam_img, max_loc = generate_gradcam(img, model)
            
            st.divider()
            col_res, col_img = st.columns([1, 1.3])
            
            with col_res:
                st.write("### Diagnosa Pakar AI:")
                if label == "KURANG SEHAT":
                    st.error(f"## {label}")
                else:
                    st.success(f"## {label}")
                
                st.metric("Tingkat Keyakinan (Confidence)", accuracy_pct)
                st.info(get_explanation(label, max_loc))
                
            with col_img:
                st.image(gradcam_img, use_container_width=True, caption=f"Hasil Analisis Grad-CAM (Akurasi: {accuracy_pct})")
                
            # Simpan Otomatis (Cek Session)
            if "last_file" not in st.session_state or st.session_state.last_file != file.name:
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{"Waktu": waktu, "Hasil": label, "Keyakinan": accuracy_pct}])
                save_to_google_sheets(new_row)
                st.session_state.last_file = file.name
                st.toast("Data otomatis dicatat!")

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
