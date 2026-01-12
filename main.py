import streamlit as st
from PIL import Image
from datetime import datetime
import pandas as pd
from utils import load_model_cloud, preprocess_image, save_to_google_sheets

# --- KONFIGURASI ---
st.set_page_config(page_title="Petani_Abies AI", layout="centered")

# Memuat model di awal agar tidak lemot
model = load_model_cloud()

st.title("🐟 Petani_Abies AI")
st.divider()

file = st.file_uploader("📤 Upload Foto Ikan", type=['jpg', 'jpeg', 'png'])

if file:
    img = Image.open(file).convert("RGB")
    
    # MEMBAGI LAYAR: Kiri untuk Foto (2 bagian), Kanan untuk Tombol (1 bagian)
    col_foto, col_aksi = st.columns([2, 1])
    
    with col_foto:
        # Menampilkan foto dengan lebar otomatis mengikuti kolom
        st.image(img, use_container_width=True, caption="Pratinjau Foto")
        
    with col_aksi:
        st.markdown("### Menu Analisis")
        # TOMBOL ANALISIS DI KANAN FOTO
        if st.button("🔍 ANALISIS SEKARANG"):
            with st.spinner("AI sedang bekerja..."):
                # 1. AI PROSES (Logika tetap sama)
                processed = preprocess_image(img)
                prediction = model.predict(processed, verbose=0)
                score = float(prediction[0][0])
                
                # 2. DEFINISIKAN VARIABEL
                waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                label = "KURANG SEHAT" if score > 0.5 else "KUALITAS BAIK"
                
                # 3. TAMPILKAN HASIL DI BAWAH TOMBOL (Masih dalam col_aksi)
                if score > 0.5:
                    st.error(f"**Hasil:**\n\n{label}")
                else:
                    st.success(f"**Hasil:**\n\n{label}")
                
                st.write(f"**Confidence Score:** `{score:.4f}`")
                
                # 4. SIMPAN KE GOOGLE SHEETS
                new_row = pd.DataFrame([{
                    "Waktu": waktu_sekarang,
                    "Hasil_Klasifikasi": label,
                    "Sigmoid_Score": score
                }])
                save_to_google_sheets(new_row)
                st.toast("✅ Tersimpan ke database!")
