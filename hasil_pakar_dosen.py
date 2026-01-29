import streamlit as st
import base64

def render_pakar_dosen():
    st.title("👨‍🔬 Dashboard Pakar Dosen")
    st.markdown("---")

    st.subheader("📄 Dokumen Validasi Kualitas Benih")
    st.write("Berikut adalah dokumen hasil penelitian: **Validasi Data Sistem Klasifikasi Kualitas Benih Ikan Mas**.")

    # Nama file harus sama persis dengan yang ada di GitHub kamu
    file_path = "hasil_pakar_dosen.pdf"

    # Kolom untuk informasi dan tombol unduh
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            
            st.success("✅ Dokumen Siap")
            st.download_button(
                label="📥 Unduh Hasil Penelitian (PDF)",
                data=pdf_bytes,
                file_name=file_path,
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error("❌ File PDF tidak ditemukan.")
            st.info("Pastikan file 'hasil_pakar_dosen.pdf' sudah ada di repositori GitHub kamu.")

    with col2:
        st.info("""
        **Informasi Dokumen:**
        - **Judul:** Klasifikasi Benih Ikan Mas dengan Algoritma CNN.
        - **Lokasi:** Kecamatan Karanggeneng, Lamongan.
        - **Peneliti:** Fatikh Afan Kurniawan.
        - **Institusi:** Universitas Islam Lamongan.
        """)

    st.divider()

    # --- FITUR PREVIEW PDF ---
    st.write("### 📖 Pratinjau Dokumen")
    
    if st.checkbox("Tampilkan Isi Dokumen Langsung"):
        try:
            with open(file_path, "rb") as f:
                # Mengubah PDF ke format base64 agar bisa ditampilkan di browser
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # Embed PDF menggunakan HTML
            pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf">'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal menampilkan pratinjau: {e}")
