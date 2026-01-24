import streamlit as st
from PIL import Image
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
        
        with st.spinner("🔍 Memvalidasi objek dan memproses analisis..."):
            # Logika Filter Bukan Ikan (Berdasarkan sebaran warna & skor AI)
            std_dev = np.std(img_np)
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])
            
            # Deteksi jika objek bukan ikan (berdasarkan keyakinan AI dan tekstur gambar)
            if (0.47 < score < 0.53) or (std_dev < 15):
                st.warning("⚠️ **Mohon maaf mas, ini sepertinya bukan foto ikan.** Silakan unggah foto benih ikan yang jelas.")
                st.image(img, use_container_width=True, caption="Objek tidak teridentifikasi sebagai benih ikan.")
            else:
                label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                confidence = score if score > 0.5 else (1 - score)
                accuracy_pct = f"{confidence * 100:.2f}%"
                
                # Cek Kondisi Ikan Kering
                is_dry = True if np.mean(img_np) > 200 else False
                
                # Generate Grad-CAM
                gradcam_img, max_loc, heatmap_raw = generate_gradcam(img, model)
                
                st.divider()
                # TATA LETAK: col_img (KIRI), col_txt (KANAN)
                col_img, col_txt = st.columns([1.3, 1])
                
                with col_img:
                    # Menampilkan Visualisasi di sebelah KIRI
                    st.image(gradcam_img, use_container_width=True, caption=f"Visualisasi Grad-CAM (Keyakinan: {accuracy_pct})")
                    
                with col_txt:
                    # Menampilkan Keterangan di sebelah KANAN
                    st.write("### Diagnosa Pakar AI:")
                    if label == "KURANG SEHAT":
                        st.error(f"## {label}")
                    else:
                        st.success(f"## {label}")
                    
                    st.metric("Tingkat Keyakinan AI", accuracy_pct)
                    st.info(get_explanation(label, max_loc, heatmap_raw, is_dry))
                    
                if "last_file" not in st.session_state or st.session_state.last_file != file.name:
                    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    new_row = pd.DataFrame([{"Waktu": waktu, "Hasil": label, "Akurasi": accuracy_pct}])
                    save_to_google_sheets(new_row)
                    st.session_state.last_file = file.name

elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
