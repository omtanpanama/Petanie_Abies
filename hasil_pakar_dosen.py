import streamlit as st
import os
import base64

def render_pakar_dosen():
    # 1. CSS Custom untuk UI Modern (Tetap dipertahankan)
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
            margin-bottom: 20px; min-height: 180px;
        }
        .status-verifikasi {
            background-color: #ECFDF5; border: 1px solid #10B981;
            color: #065F46; padding: 12px; border-radius: 8px;
            text-align: center; margin: 20px 0; font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # 2. Header
    st.markdown('<div class="main-header"><h2 style="margin:0; color: white;">👨‍🔬 Dashboard Validasi Pakar</h2></div>', unsafe_allow_html=True)

    # 3. Info Panel (Gaya Card)
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        st.markdown("""<div class="pakar-card"><b>🔬 JUDUL PENELITIAN</b><br>Klasifikasi Benih Ikan Mas Dengan Algoritma CNN</div>""", unsafe_allow_html=True)
    with col_info2:
        st.markdown("""<div class="pakar-card"><b>🎓 NARASUMBER AHLI</b><br>Fuquh Rahmat Shaleh, S.Pi., M.Si.</div>""", unsafe_allow_html=True)

    # 4. Status & Foto
    st.markdown('<div class="status-verifikasi">✅ STATUS: Dokumen ini telah diverifikasi secara sah.</div>', unsafe_allow_html=True)
    
    col_img1, col_img2 = st.columns(2)
    if os.path.exists("pak_fuquh01.jpeg"):
        col_img1.image("pak_fuquh01.jpeg", caption="Dokumentasi I", use_container_width=True)
    if os.path.exists("pak_fuquh02.jpeg"):
        col_img2.image("pak_fuquh02.jpeg", caption="Dokumentasi II", use_container_width=True)

    st.divider()

    # 5. PERBAIKAN PREVIEW PDF (Menggunakan Base64)
    st.subheader("📖 Eksplorasi Dokumen PDF")
    
    pdf_file = "hasil_pakar_dosen.pdf"
    
    if os.path.exists(pdf_file):
        with open(pdf_file, "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
        
        # PDF Display menggunakan data base64 (lebih aman dan pasti muncul)
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf" style="border-radius:10px; border:1px solid #ddd;"></iframe>'
        
        tab1, tab2 = st.tabs(["📄 Pratinjau Langsung", "📥 Opsi Unduhan"])
        with tab1:
            st.markdown(pdf_display, unsafe_allow_html=True)
        with tab2:
            with open(pdf_file, "rb") as f:
                st.download_button("💾 Unduh File PDF", f, file_name=pdf_file, mime="application/pdf", use_container_width=True)
    else:
        st.error(f"File '{pdf_file}' tidak ditemukan di server. Pastikan file sudah di-upload ke GitHub.")

    st.caption("© 2026 Petani_Abies AI")
