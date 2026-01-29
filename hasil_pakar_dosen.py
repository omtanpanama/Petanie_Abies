import streamlit as st

def render_pakar_dosen():
    st.title("👨‍🔬 Dashboard Pakar Dosen")
    st.markdown("---")

    # 1. KARTU INFORMASI UTAMA (Agar data langsung terbaca tanpa PDF)
    st.subheader("📌 Detail Validasi Dokumen")
    
    # Menggunakan container untuk tampilan yang lebih profesional
    with st.container():
        col_meta1, col_meta2 = st.columns(2)
        
        with col_meta1:
            st.markdown(f"""
            **Informasi Penelitian:**
            * **Judul:** Klasifikasi Benih Ikan Mas Dengan Algoritma CNN Berbasis Python
            * **Lokasi:** Toko Barokah, Kec. Karanggeneng, Lamongan
            * **Peneliti:** Fatikh Afan Kurniawan
            """)
        
        with col_meta2:
            st.markdown(f"""
            **Validasi Pakar:**
            * **Narasumber:** Fuquh Rahmat Shaleh, S.Pi., M.Si.
            * **Jabatan:** Wakil Dekan 1 Fakultas Perikanan & Peternakan UNISLA
            * **Tanggal:** 12 Januari 2026
            """)

    st.success("✅ Dokumen ini telah divalidasi sebagai bukti keaslian data sistem Petani_Abies.")
    
    st.divider()

    # 2. SEKSI DOWNLOAD (Cara paling aman jika Preview diblokir browser)
    st.subheader("📄 Dokumen Fisik (PDF)")
    file_path = "hasil_pakar_dosen.pdf"

    try:
        with open(file_path, "rb") as f:
            pdf_bytes = f.read()
        
        st.write("Jika pratinjau di bawah tidak muncul karena batasan keamanan browser Anda, silakan unduh dokumen melalui tombol di bawah ini:")
        st.download_button(
            label="📥 Unduh & Simpan Dokumen PDF",
            data=pdf_bytes,
            file_name=file_path,
            mime="application/pdf",
            use_container_width=True
        )
    except FileNotFoundError:
        st.error("❌ File PDF 'hasil_pakar_dosen.pdf' tidak ditemukan di server.")

    st.divider()

    # 3. PRATINJAU (Versi Link Eksternal - Lebih Stabil)
    st.subheader("📖 Pratinjau Dokumen")
    
    # Kita berikan instruksi jika masih tidak muncul
    st.warning("⚠️ Jika layar di bawah tetap kosong, silakan klik tombol 'Unduh' di atas untuk melihat dokumen.")

    # Gunakan link langsung ke file di GitHub agar Chrome tidak memblokir base64
    # Ganti URL ini dengan URL Raw file PDF kamu di GitHub
    pdf_url = "https://raw.githubusercontent.com/omtanpanama/Petanie_Abies/main/hasil_pakar_dosen.pdf"
    
    # Embed menggunakan PDF viewer Google Docs agar lebih kompatibel
    st.markdown(f'''
        <iframe src="https://docs.google.com/viewer?url={pdf_url}&embedded=true" 
                width="100%" height="800" style="border: none;">
        </iframe>
    ''', unsafe_allow_html=True)
