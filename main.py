import streamlit as st
from PIL import Image, ImageStat
from datetime import datetime
import pandas as pd
import numpy as np

from styles import apply_custom_css, render_footer
from utils import (
    load_model_cloud,
    preprocess_image,
    save_to_google_sheets,
    generate_gradcam,
    get_explanation
)
from admin_page import show_navbar, render_admin_login, render_dashboard


# ===============================
# KONFIGURASI AWAL
# ===============================
st.set_page_config(
    page_title="Petani_Abies AI",
    layout="wide"
)
apply_custom_css()

try:
    model = load_model_cloud()
except Exception as e:
    st.error(f"Gagal memuat sistem AI: {e}")
    st.stop()


choice, sub_choice = show_navbar()
st.markdown('<div class="main-content">', unsafe_allow_html=True)


# ===============================
# HALAMAN UTAMA (PETANI)
# ===============================
if choice == "🏠 Halaman Utama":

    st.title("🐟 Scan Kualitas Benih Otomatis")
    st.caption("Unggah foto benih ikan, AI akan menganalisis kualitas secara otomatis.")

    file = st.file_uploader(
        "📤 Unggah Foto Ikan",
        type=["jpg", "jpeg", "png"]
    )

    if file:
        img = Image.open(file).convert("RGB")
        img_np = np.array(img)

        with st.spinner("🔍 AI sedang menganalisis foto..."):

            # ===============================
            # VALIDASI GAMBAR (ANTI SCREENSHOT / TEKS)
            # ===============================
            std_dev = np.std(img_np)
            mean_val = np.mean(img_np)

            stat = ImageStat.Stat(img)
            saturation = sum(stat.var) / len(stat.var)

            is_text_or_jurnal = (mean_val > 160 and saturation < 1200)
            is_coding_screen = (std_dev > 50 and mean_val < 100)
            is_too_flat = (std_dev < 10)

            if is_text_or_jurnal or is_coding_screen or is_too_flat:
                st.warning("⚠️ Foto terdeteksi BUKAN foto ikan.")
                st.info("Pastikan yang diunggah adalah foto benih ikan asli, bukan screenshot atau dokumen.")
                st.stop()


            # ===============================
            # PREDIKSI MODEL
            # ===============================
            processed = preprocess_image(img)
            prediction = model.predict(processed, verbose=0)
            score = float(prediction[0][0])

            label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
            confidence = score if score > 0.5 else (1 - score)
            accuracy_pct = f"{confidence * 100:.2f}%"

            is_dry = mean_val > 215


            # ===============================
            # GRAD-CAM (TIDAK LONJONG)
            # ===============================
            gradcam_img, max_loc, heatmap_raw = generate_gradcam(img, model)


        # ===============================
        # TAMPILAN HASIL (HANYA GRAD-CAM)
        # ===============================
        st.divider()

        st.subheader("🔥 Fokus Analisis AI")
        st.image(
            gradcam_img,
            use_container_width=True,
            caption=f"Area paling berpengaruh dalam penilaian AI (Keyakinan: {accuracy_pct})"
        )

        st.divider()


        # ===============================
        # HASIL & PENJELASAN
        # ===============================
        col_hasil, col_pakar = st.columns([1, 1.6])

        with col_hasil:
            st.write("### Hasil Diagnosa")
            if label == "KURANG SEHAT":
                st.error(f"## {label}")
            else:
                st.success(f"## {label}")

            st.metric("Keyakinan AI", accuracy_pct)

        with col_pakar:
            st.write("### Penjelasan Pakar AI")
            st.info(
                get_explanation(
                    label=label,
                    max_loc=max_loc,
                    heatmap_raw=heatmap_raw,
                    is_dry=is_dry
                )
            )


        # ===============================
        # SIMPAN KE GOOGLE SHEETS
        # ===============================
        try:
            if st.session_state.get("last_file") != file.name:
                waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                new_row = pd.DataFrame([{
                    "Waktu": waktu,
                    "Hasil": label,
                    "Keyakinan": accuracy_pct
                }])
                save_to_google_sheets(new_row)
                st.session_state.last_file = file.name
        except Exception as e:
            st.warning(f"Data tidak tersimpan ke database: {e}")


# ===============================
# HALAMAN ADMIN
# ===============================
elif choice == "🛡️ Admin":
    if render_admin_login():
        render_dashboard()


st.markdown('</div>', unsafe_allow_html=True)
render_footer()
