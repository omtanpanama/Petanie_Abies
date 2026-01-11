import streamlit as st
from PIL import Image
from datetime import datetime
from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image
from admin_page import show_admin_sidebar, render_dashboard

st.set_page_config(page_title="Petani_Abies AI", layout="centered")
apply_custom_css()

if 'history' not in st.session_state: st.session_state.history = []

model = load_model_cloud()
choice = show_admin_sidebar()

st.markdown('<div class="main-content">', unsafe_allow_html=True)

if st.session_state.get('logged_in') and choice == "📊 Dashboard Laporan":
    render_dashboard()
else:
    st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Petani_Abies AI</h1>", unsafe_allow_html=True)
    st.divider()

    file = st.file_uploader("📤 Upload Foto Ikan", type=['jpg', 'jpeg', 'png'])
    if file:
        img = Image.open(file).convert("RGB")
        st.image(img, use_container_width=True)
        
        if st.button("🔍 ANALISIS SEKARANG"):
            with st.spinner("AI sedang memproses Sigmoid..."):
                processed = preprocess_image(img)
                prediction = model.predict(processed, verbose=0)
                score = float(prediction[0][0]) # Output Sigmoid (0-1)
                
                # Penentuan Label (Sigmoid Standard)
                if score > 0.5:
                    label = "KURANG SEHAT"
                    color = "error"
                else:
                    label = "KUALITAS BAIK"
                    color = "success"
                
                # Menampilkan Hasil
                getattr(st, color)(f"### Hasil: {label}")
                st.write(f"**AI Confidence Score (Sigmoid):** `{score:.4f}`")
                
                # Simpan ke histori
                st.session_state.history.append({
                    "Waktu": datetime.now().strftime("%H:%M:%S"),
                    "Hasil": label,
                    "Sigmoid_Score": round(score, 4)
                })

st.markdown('</div>', unsafe_allow_html=True)
render_footer()
