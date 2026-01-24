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
    st.error(f"Gagal memuat model AI: {e}")
    st.stop()

choice, sub_choice = show_navbar()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

if choice == "🏠 Halaman Utama":
    st.title("🐟 Deteksi Kualitas Benih Ikan")
    file = st.file_uploader("📤 Unggah Foto Benih (JPG/PNG)", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        image_placeholder = st.empty()
        
        # Simpan state file agar tidak reload terus menerus
        if "current_file" not in st.session_state or st.session_state.current_file != file.name:
            image_placeholder.image(img, use_container_width=True, caption="Pratinjau Foto")
            st.session_state.is_processed = False

        if st.button("🔍 MULAI ANALISIS"):
            with st.spinner("AI sedang menganalisis morfologi ikan..."):
                image_placeholder.empty() # Sembunyikan foto asli
                
                # Menghitung Prediksi
                processed = preprocess_image(img)
                prediction = model.predict(processed, verbose=0)
                score = float(prediction[0][0]) # Output Sigmoid (0.0 - 1.0)
                
                # Logika Sigmoid: 
                # > 0.5 = Kurang Sehat (Mendekati 1.0)
                # < 0.5 = Kualitas Baik (Mendekati 0.0)
                label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                
                # Hitung Akurasi Keyakinan (Confidence Score)
                confidence = score if score > 0.5 else (1 - score)
                accuracy_text = f"{confidence * 100:.2f}%"
                
                # Jalankan Grad-CAM
                gradcam_img, max_loc = generate_gradcam(img, model)
                
                # TAMPILAN OUTPUT
                st.divider()
                col_res, col_img = st.columns([1, 1.2])
                
                with col_res:
                    st.write("### Hasil Diagnosis Pakar AI:")
                    if label == "KURANG SEHAT":
                        st.error(f"## {label}")
                    else:
                        st.success(f"## {label}")
                    
                    st.metric("Tingkat Keyakinan Model", accuracy_text)
                    st.markdown(get_explanation(label, max_loc))
                    
                with col_img:
                    st.image(gradcam_img, use_container_width=True, caption="Visualisasi Deteksi (Explainable AI)")

                # Simpan ke Database
                st.session_state.current_file = file.name
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{"Waktu": waktu, "Hasil": label, "Akurasi": accuracy_text}])
                save_to_google_sheets(new_row)
                st.toast("Data hasil analisis telah tersimpan.")

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
