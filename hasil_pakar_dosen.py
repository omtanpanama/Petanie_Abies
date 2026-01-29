import streamlit as st
import base64

def render_pakar_dosen():
    st.title("👨‍🔬 Dashboard Pakar Dosen")
    st.markdown("---")

    st.subheader("📄 Dokumen Validasi Kualitas Benih")
    st.write("Berikut adalah dokumen hasil penelitian: **Validasi Data Sistem Klasifikasi Kualitas Benih Ikan Mas**.")

    # Nama file sesuai dengan yang ada di GitHub kamu
    file_path = "hasil_pakar_dosen.pdf"

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

    with col2:
        st.info("""
        **Informasi Dokumen:**
        - **Judul:** Klasifikasi Benih Ikan Mas dengan Algoritma CNN.
        - **Peneliti:** Fatikh Afan Kurniawan.
        - **Institusi:** Universitas Islam Lamongan.
        """)

    st.divider()
    st.write("### 📖 Pratinjau Dokumen")
    
    if st.checkbox("Tampilkan Isi Dokumen Langsung"):
        try:
            with open(file_path, "rb") as f:
                base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            
            # MENGGUNAKAN IFRAME (Lebih stabil daripada EMBED)
            pdf_display = f'''
                <iframe src="data:application/pdf;base64,{base64_pdf}" 
                        width="100%" height="800" 
                        type="application/pdf"
                        style="border: none;">
                </iframe>
            '''
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Gagal menampilkan pratinjau: {e}")
