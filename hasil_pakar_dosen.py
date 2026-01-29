import streamlit as st
import os

def render_pakar_dosen():
    # 1. CSS Custom untuk UI Modern
    st.markdown("""
        <style>
        .main-header {
            text-align: center; padding: 20px;
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
            color: white; border-radius: 15px; margin-bottom: 25px;
        }
        .pakar-card {
            background-color: #ffffff; padding: 20px;
            border-radius: 12px; border-left: 5px solid #3B82F6;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 20px; min-height: 200px;
        }
        .pakar-label { font-weight: bold; color: #1E3A8A; font-size: 0.85rem; }
        .status-verifikasi {
            background-color: #ECFDF5; border: 1px solid #10B981;
            color: #065F46; padding: 12px; border-radius: 8px;
            text-align: center; margin: 20px 0; font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Header
    st.markdown("""
        <div class="main-header">
            <h2 style="margin:0; color: white;">👨‍🔬 Dashboard Validasi Pakar</h2>
            <p style="margin:0; opacity: 0.8;">Verifikasi Akademis & Dokumentasi Penelitian</p>
        </div>
    """, unsafe_allow_html=True)

    # 3. Info Panel
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown(f"""
            <div class="pakar-card">
                <p><span class="pakar-label">🔬 JUDUL PENELITIAN</span><br>
                <b>Klasifikasi Benih Ikan Mas Dengan Algoritma CNN Berbasis Python</b></p>
                <p><span class="pakar-label">📍 LOKASI STUDI</span><br>
                Toko Barokah, Kec. Karanggeneng, Lamongan</p>
            </div>
        """, unsafe_allow_html=True)

    with col_info2:
        st.markdown(f"""
            <div class="pakar-card">
                <p><span class="pakar-label">🎓 NARASUMBER AHLI</span><br>
                <b>Fuquh Rahmat Shaleh, S.Pi., M.Si.</b></p>
                <p><span class="pakar-label">🏛️ INSTITUSI</span><br>
                Fakultas Perikanan & Peternakan UNISLA</p>
            </div>
        """, unsafe_allow_html=True)

    # 4. Status & Foto Dokumentasi
    st.markdown('<div class="status-verifikasi">✅ STATUS: Dokumen ini telah diverifikasi secara sah oleh otoritas akademis terkait.</div>', unsafe_allow_html=True)

    # Menampilkan Foto dengan Pengecekan Keberadaan File
    col_img1, col_img2 = st.columns(2)
    
    img1_path = "pak_fuquh01.jpeg"
    img2_path = "pak_fuquh02.jpeg"

    with col_img1:
        if os.path.exists(img1_path):
            st.image(img1_path, caption="Dokumentasi Validasi I", use_container_width=True)
        else:
            st.error(f"⚠️ File {img1_path} tidak ditemukan.")

    with col_img2:
        if os.path.exists(img2_path):
            st.image(img2_path, caption="Dokumentasi Validasi II", use_container_width=True)
        else:
            st.error(f"⚠️ File {img2_path} tidak ditemukan.")

    st.divider()

    # 5. Preview PDF
    st.subheader("📖 Eksplorasi Dokumen PDF")
    tab1, tab2 = st.tabs(["📄 Pratinjau Langsung", "📥 Opsi Unduhan"])

    with tab1:
        pdf_url = "https://raw.githubusercontent.com/omtanpanama/Petanie_Abies/main/hasil_pakar_dosen.pdf"
        st.markdown(f'''
            <iframe src="https://docs.google.com/viewer?url={pdf_url}&embedded=true" 
                    width="100%" height="600" style="border: 1px solid #EEE; border-radius:10px;">
            </iframe>
        ''', unsafe_allow_html=True)

    with tab2:
        if os.path.exists("hasil_pakar_dosen.pdf"):
            with open("hasil_pakar_dosen.pdf", "rb") as f:
                st.download_button("💾 Unduh Berita Acara (PDF)", f, file_name="hasil_pakar_dosen.pdf", mime="application/pdf", use_container_width=True)
        else:
            st.warning("File PDF belum tersedia di server.")

    st.caption("© 2026 Petani_Abies AI - System Module")
