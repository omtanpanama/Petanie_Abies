import streamlit as st
from PIL import Image
from datetime import datetime

from styles import apply_custom_css, render_footer
from utils import load_model_cloud, preprocess_image
from admin_page import show_admin_sidebar, render_dashboard, render_info


# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Petani_Abies AI",
    layout="centered",
    page_icon="🐟"
)

apply_custom_css()


# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ---------------- LOAD MODEL (ONCE) ----------------
@st.cache_resource
def load_model():
    return load_model_cloud()

model = load_model()


# ---------------- SIDEBAR ----------------
choice = show_admin_sidebar()


# ================== MAIN CONTENT ==================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# ========== ADMIN MODE ==========
if st.session_state.logged_in:

    if choice == "📊 Dashboard Laporan":
        render_dashboard()

    elif choice == "ℹ️ Informasi Aplikasi":
        render_info()

    else:
        st.info("Silakan pilih menu admin di sidebar.")

# ========== USER / PETANI MODE ==========
else:
    st.markdown(
        "<h1 style='text-align:center;color:#1e3a8a;'>🐟 Petani_Abies AI</h1>",
        unsafe_allow_html=True
    )
    st.caption("Sistem AI untuk analisis kualitas ikan berbasis citra")
    st.divider()

    file = st.file_uploader(
        "📤 Upload Foto Ikan",
        type=["jpg", "jpeg", "png"]
    )

    if file is not None:
        try:
            img = Image.open(file).convert("RGB")
            st.image(img, use_container_width=True)

            if st.button("🔍 ANALISIS SEKARANG", use_container_width=True):
                with st.spinner("AI sedang menganalisis kualitas ikan..."):
                    processed = preprocess_image(img)
                    prediction = model.predict(processed, verbose=0)
                    score = float(prediction[0][0])  # Sigmoid (0–1)

                    # ---- Klasifikasi ----
                    if score > 0.5:
                        label = "KURANG SEHAT"
                        st.error(f"### ❌ Hasil: {label}")
                    else:
                        label = "KUALITAS BAIK"
                        st.success(f"### ✅ Hasil: {label}")

                    st.write(f"**Confidence Score (Sigmoid):** `{score:.4f}`")

                    # ---- Simpan histori ----
                    st.session_state.history.append({
                        "Waktu": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
                        "Hasil": label,
                        "Sigmoid_Score": round(score, 4)
                    })

        except Exception as e:
            st.error("Gagal membaca gambar. Pastikan file valid.")
            st.caption(str(e))


st.markdown('</div>', unsafe_allow_html=True)
render_footer()
