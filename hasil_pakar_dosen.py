import streamlit as st

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
            st.success("✅ Dokumen Siap")
            st.download_button(
                label="📥 Unduh Hasil Penelitian (PDF)",
                data=pdf_bytes,
                file_name=file_path,
                mime="application/pdf"
            )
        except FileNotFoundError:
            st.error("❌ File PDF tidak ditemukan di server.")

    with col2:
        st.info("""
        **Informasi Dokumen:**
        - **Judul:** Klasifikasi Benih Ikan Mas dengan Algoritma CNN.
        - **Peneliti:** Fatikh Afan Kurniawan.
        - **Institusi:** Universitas Islam Lamongan.
        """)

    st.divider()
    
    # --- SOLUSI PRATINJAU STABIL ---
    st.write("### 📖 Pratinjau Dokumen")
    
    # Menampilkan PDF menggunakan Iframe standar Streamlit yang lebih ringan
    # Jika cara base64 diblokir, kita gunakan PDF viewer dari Google Docs secara eksternal
    if st.checkbox("Tampilkan Isi Dokumen"):
        # Karena file ada di GitHub, kita panggil link mentahnya (raw)
        # Ganti 'username' dan 'repo' sesuai dengan akun GitHub kamu
        raw_pdf_url = "https://raw.githubusercontent.com/omtanpanama/Petanie_Abies/main/hasil_pakar_dosen.pdf"
        
        # Link Google Docs Viewer agar tidak diblokir browser
        google_view_url = f"https://docs.google.com/viewer?url={raw_pdf_url}&embedded=true"
        
        st.markdown(f'''
            <iframe src="{google_view_url}" width="100%" height="800" style="border: none;">
            </iframe>
        ''', unsafe_allow_html=True)
