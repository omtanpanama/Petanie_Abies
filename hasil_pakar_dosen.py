import streamlit as st

def render_pakar_dosen():
    # Header dengan Ikon Besar
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #1E3A8A;">👨‍🔬 Dashboard Validasi Pakar</h1>
            <p style="color: #64748B; font-size: 18px;">Dokumentasi Saintifik & Verifikasi Akademis</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")

    # 1. KARTU INFORMASI UTAMA (Gaya Glassmorphism Sederhana)
    st.subheader("📌 Resume Eksekutif Penelitian")
    
    # Membuat background kotak yang lebih cantik dengan CSS inline
    st.markdown("""
        <style>
        .pakar-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 15px;
            border-left: 10px solid #1E3A8A;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px;
        }
        .pakar-label { font-weight: bold; color: #1E3A8A; }
        </style>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown(f"""
            <div class="pakar-card">
                <p><span class="pakar-label">🔬 Judul Penelitian:</span><br>
                Klasifikasi Benih Ikan Mas Dengan Algoritma CNN Berbasis Python</p>
                <p><span class="pakar-label">📍 Lokasi Studi:</span><br>
                Toko Barokah, Kec. Karanggeneng, Lamongan</p>
                <p><span class="pakar-label">👤 Peneliti Utama:</span><br>
                Fatikh Afan Kurniawan</p>
            </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
            <div class="pakar-card">
                <p><span class="pakar-label">🎓 Narasumber Ahli:</span><br>
                Fuquh Rahmat Shaleh, S.Pi., M.Si.</p>
                <p><span class="pakar-label">🏛️ Institusi:</span><br>
                Fakultas Perikanan & Peternakan UNISLA</p>
                <p><span class="pakar-label">📅 Tanggal Validasi:</span><br>
                12 Januari 2026</p>
            </div>
        """, unsafe_allow_html=True)

    # Status Approval
    st.success("✅ **STATUS:** Dokumen ini telah diverifikasi secara sah oleh otoritas akademis terkait.")

    st.divider()

    # 2. SEKSI DOKUMEN & PREVIEW
    st.subheader("📖 Eksplorasi Dokumen PDF")
    
    tab1, tab2 = st.tabs(["📄 Pratinjau Langsung", "📥 Opsi Unduhan"])

    with tab1:
        # Gunakan link Raw GitHub kamu
        pdf_url = "https://raw.githubusercontent.com/omtanpanama/Petanie_Abies/main/hasil_pakar_dosen.pdf"
        
        st.warning("⚠️ Jika dokumen tidak muncul, browser Anda mungkin memblokir pratinjau. Gunakan tab 'Opsi Unduhan'.")
        
        # Embed dengan bingkai yang lebih rapi
        st.markdown(f'''
            <div style="border: 2px solid #E2E8F0; border-radius: 10px; overflow: hidden;">
                <iframe src="https://docs.google.com/viewer?url={pdf_url}&embedded=true" 
                        width="100%" height="800" style="border: none;">
                </iframe>
            </div>
        ''', unsafe_allow_html=True)

    with tab2:
        st.write("Klik tombol di bawah untuk menyimpan dokumen secara offline.")
        file_path = "hasil_pakar_dosen.pdf"
        try:
            with open(file_path, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="💾 Simpan Dokumen (PDF)",
                data=pdf_bytes,
                file_name=file_path,
                mime="application/pdf",
                use_container_width=True
            )
        except FileNotFoundError:
            st.error("File fisik tidak ditemukan di server.")

    st.divider()
    
    # 3. FOOTER KHUSUS ADMIN
    st.caption("Petani_Abies AI System - Academic Validation Module v1.0")
