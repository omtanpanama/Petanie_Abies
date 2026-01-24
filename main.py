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
    st.title("🐟 Sistem Deteksi Kualitas Benih")
    file = st.file_uploader("📤 Upload Foto Ikan", type=['jpg', 'jpeg', 'png'])
    
    if file:
        img = Image.open(file).convert("RGB")
        
        # Tempat untuk menampilkan foto yang bisa di-update
        image_placeholder = st.empty()
        
        # Cek apakah sudah di-analisis
        if "analyzed_file" not in st.session_state or st.session_state.analyzed_file != file.name:
            image_placeholder.image(img, use_container_width=True, caption="Pratinjau Foto Asli")
            st.session_state.is_analyzed = False
        
        if st.button("🔍 ANALISIS SEKARANG"):
            with st.spinner("AI sedang menganalisis bagian tubuh ikan..."):
                # Menghapus foto asli dari tampilan
                image_placeholder.empty()
                
                # Proses Prediksi & Grad-CAM
                processed = preprocess_image(img)
                prediction = model.predict(processed, verbose=0)
                score = float(prediction[0][0])
                
                gradcam_img, max_loc = generate_gradcam(img, model)
                label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                
                # Menampilkan Hasil Visual Grad-CAM
                st.subheader(f"Hasil Klasifikasi: {label}")
                st.image(gradcam_img, use_container_width=True, caption="Visualisasi Grad-CAM (Area Merah = Fokus Utama AI)")
                
                # Menampilkan Teks Penjelasan Spesifik
                penjelasan = get_explanation(label, max_loc)
                if score > 0.5:
                    st.error(penjelasan)
                else:
                    st.success(penjelasan)
                
                # Simpan data
                st.session_state.analyzed_file = file.name
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{"Waktu": waktu_sekarang, "Hasil_Klasifikasi": label, "Sigmoid_Score": score}])
                save_to_google_sheets(new_row)
                st.toast("Analisis Selesai!")

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

elif choice == "👨‍🔬 Hasil Pakar":
    st.title(f"👨‍🔬 Halaman {sub_choice}")
    st.info("Data riwayat pakar sedang dalam tahap sinkronisasi.")

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
