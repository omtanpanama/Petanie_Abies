import streamlit as st

def render_pakar_dosen():
    # 1. Konfigurasi Gaya (CSS Injection)
    st.markdown("""
        <style>
        .main-header {
            text-align: center; 
            padding: 25px;
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: white;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        .section-header {
            color: #1E3A8A;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 10px;
            margin-top: 20px;
        }
        .pakar-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            border-top: 5px solid #3B82F6;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            height: 100%;
        }
        .pakar-label { 
            font-weight: bold; 
            color: #1E3A8A; 
            text-transform: uppercase;
            font-size: 0.8rem;
        }
        .status-box {
            background-color: #F0FDF4;
            border: 1px solid #BBF7D0;
            color: #166534;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: 500;
            margin: 20px 0;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Header Dashboard
    st.markdown("""
        <div class="main-header">
            <h1 style="margin:0; color: white;">👨‍🔬 Dashboard Validasi Pakar</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">Sistem Informasi Verifikasi Akademis & Saintifik</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Resume Eksekutif (Grid Layout)
    st.markdown('<h3 class="section-header">📌 Resume Eksekutif Penelitian</h3>', unsafe_allow_html=True)
    
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"""
            <div class="pakar-card">
                <p><span class="pakar-label">🔬 Judul Penelitian</span><br>
                <b>Klasifikasi Benih Ikan Mas Dengan Algoritma CNN Berbasis Python</b></p>
                <p><span class="pakar-label">📍 Lokasi Studi</span><br>
                Toko Barokah, Kec. Karanggeneng, Lamongan</p>
                <p><span class="pakar-label">👤 Peneliti Utama</span><br>
                Fatikh Afan Kurniawan</p>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
            <div class="pakar-card">
                <p><span class="pakar-label">🎓 Narasumber Ahli</span><br>
                <b>Fuquh Rahmat Shaleh, S.Pi., M.Si.</b></p>
                <p><span class="pakar-label">🏛️ Institusi</span><br>
                Fakultas Perikanan & Peternakan UNISLA</p>
                <p><span class="pakar-label">📅 Tanggal Validasi</span><br>
                12 Januari 2026</p>
            </div>
        """, unsafe_allow_html=True)

    # 4. Status Approval & Dokumentasi Foto
    st.markdown("""
        <div class="status-box">
            ✅ <b>STATUS:</b> Dokumen ini telah diverifikasi secara sah oleh otoritas akademis terkait.
        </div>
    """, unsafe_allow_html=True)

    # Menampilkan Foto Pak Fuquh dengan layout yang rapi
    col_img1, col_img2 = st.columns(2)
    with col_img1:
        st.image("pak_fuquh01.jpeg", caption="Dokumentasi Validasi 01", use_container_width=True)
    with col_img2:
        st.image("pak_fuquh02.jpeg", caption="Dokumentasi Validasi 02", use_container_width=True)

    # 5. Eksplorasi Dokumen PDF
    st.markdown('<h3 class="section-header">📖 Eksplorasi Dokumen PDF</h3>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📄 Pratinjau Interaktif", "📥 Pusat Unduhan"])

    with tab1:
        pdf_url = "https://raw.githubusercontent.com/omtanpanama/Petanie_Abies/main/hasil_pakar_dosen.pdf"
        st.info("💡 Gunakan panel di bawah untuk membaca dokumen secara langsung.")
        
        st.markdown(f'''
            <div style="border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
                <iframe src="https://docs.google.com/viewer?url={pdf_url}&embedded=true" 
                        width="100%" height="700" style="border: none;">
                </iframe>
            </div>
        ''', unsafe_allow_html=True)

    with tab2:
        st.write("Silahkan unduh file untuk kebutuhan arsip fisik atau cetak.")
        file_path = "hasil_pakar_dosen.pdf"
        try:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📥 Download Berita Acara (PDF)",
                data=pdf_bytes,
                file_name=file_name,
                mime="application/pdf",
                use_container_width=True
            )
        except:
            st.error("Gagal memuat file PDF. Pastikan file tersedia di direktori utama.")

    # 6. Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #94A3B8; font-size: 0.8rem;'>"
        "Petani_Abies AI System • Academic Validation Module v1.0 • 2026</div>", 
        unsafe_allow_html=True
    )
