import streamlit as st
import base64

def render_pakar_dosen():
    st.title("👨‍🔬 Dashboard Pakar Dosen")
    st.markdown("---")

    st.subheader("📄 Dokumen Validasi Kualitas Benih")
    st.write("Berikut adalah dokumen hasil penelitian: **Validasi Data Sistem Klasifikasi Kualitas Benih Ikan Mas**.")

    file_path = "hasil_pakar_dosen.pdf"

    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            st.success("✅ Dokumen Tervalidasi")
            st.download_button(
                label="📥 Unduh Hasil Penelitian (PDF)",
                data=pdf_bytes,
                file_name=file_path,
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error("❌ File PDF tidak ditemukan.")

    with col2:
        # DATA BERDASARKAN TANDA TANGAN VALIDASI DOKUMEN
        st.info("""
        **Informasi Dokumen & Validasi:**
        - **Judul Proyek:** Klasifikasi Benih Ikan Mas Dengan Algoritma CNN Berbasis Python.
        - **Lokasi Proyek:** Toko Barokah, Kecamatan Karanggeneng, Lamongan.
        - **Pakar / Narasumber:** Fuquh Rahmat Shaleh, S.Pi., M.Si. (Wakil Dekan 1 Fakultas Perikanan & Peternakan Unisla).
        - **Peneliti / Pembuat:** Fatikh Afan Kurniawan.
        - **Tanggal Validasi:** 12 Januari 2026.
        """)

    st.divider()
    
    # --- PRATINJAU DOKUMEN ---
    st.write("### 📖 Pratinjau Dokumen")
    
    if st.checkbox("Tampilkan Isi Dokumen Langsung", value=True): # Kita set True agar otomatis terbuka
        try:
            with open(file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # Menggunakan Iframe untuk stabilitas pratinjau
            pdf_display = f'''
                <iframe src="data:application/pdf;base64,{base64_pdf}" 
                        width="100%" height="900" 
                        type="application/pdf"
                        style="border: 2px solid #eee; border-radius: 10px;">
                </iframe>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal menampilkan pratinjau: {e}")
