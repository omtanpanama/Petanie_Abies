import streamlit as st
import base64

def render_pakar_dosen():
    # Header Mewah dengan Animasi Gradient (CSS)
    st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(90deg, #1E3A8A 0%, #3B82F6 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
            box-shadow: 0 4px 15px rgba(30, 58, 138, 0.2);
        }
        .pakar-card {
            background-color: #f8fafc;
            padding: 20px;
            border-radius: 12px;
            border-top: 5px solid #1E3A8A;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            height: 100%;
        }
        .pakar-label { font-weight: bold; color: #1E3A8A; display: block; margin-bottom: 5px; }
        </style>
        <div class="main-header">
            <h1 style="margin:0; color:white;">👨‍🔬 Dashboard Validasi Pakar</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">Sertifikasi Akademis & Dokumentasi Teknis Sistem</p>
        </div>
    """, unsafe_allow_html=True)

    # 1. KARTU INFORMASI (Resume Eksekutif)
    st.subheader("📌 Resume Validasi Dokumen")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
            <div class="pakar-card">
                <span class="pakar-label">🔬 Judul Penelitian:</span>
                Klasifikasi Benih Ikan Mas Dengan Algoritma CNN (Studi Kasus: Karanggeneng)
                <br><br>
                <span class="pakar-label">👤 Peneliti Utama:</span>
                Fatikh Afan Kurniawan
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="pakar-card">
                <span class="pakar-label">🎓 Narasumber Ahli:</span>
                Fuquh Rahmat Shaleh, S.Pi., M.Si. (Wakil Dekan 1 FPP Unisla)
                <br><br>
                <span class="pakar-label">📅 Tanggal Pengesahan:</span>
                12 Januari 2026
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.success("✅ **STATUS VALIDASI:** Dokumen ini sah dan telah diuji secara akademis untuk diintegrasikan ke sistem AI Petani_Abies.")

    st.divider()

    # 2. EKSPLORASI DOKUMEN PDF
    st.subheader("📖 Eksplorasi Dokumen PDF")
    
    file_path = "hasil_pakar_dosen.pdf"
    
    tab1, tab2 = st.tabs(["📄 Pratinjau Dokumen", "📥 Opsi Unduhan"])

    with tab1:
        try:
            with open(file_path, "rb") as f:
                pdf_data = f.read()
                base64_pdf = base64.b64encode(pdf_data).decode('utf-8')
            
            # --- SOLUSI AGAR TIDAK DIBLOKIR: MENGGUNAKAN OBJECT DATA ---
            # Cara ini lebih kompatibel dengan browser modern dibanding iframe murni
            pdf_display = f"""
                <div style="border: 2px solid #E2E8F0; border-radius: 10px; overflow: hidden; background: #eee;">
                    <object data="data:application/pdf;base64,{base64_pdf}" type="application/pdf" width="100%" height="900px">
                        <div style="padding: 20px; text-align: center;">
                            <p>Browser Anda tidak mendukung pratinjau PDF langsung.</p>
                            <a href="data:application/pdf;base64,{base64_pdf}" download="{file_path}" 
                               style="padding: 10px 20px; background: #1E3A8A; color: white; text-decoration: none; border-radius: 5px;">
                               Buka Dokumen Secara Manual
                            </a>
                        </div>
                    </object>
                </div>
            """
            st.markdown(pdf_display, unsafe_allow_html=True)
            
        except FileNotFoundError:
            st.error("❌ File 'hasil_pakar_dosen.pdf' tidak ditemukan di server.")

    with tab2:
        st.info("Gunakan tombol di bawah ini jika Anda ingin menyimpan dokumen ke perangkat Anda.")
        try:
            with open(file_path, "rb") as f:
                st.download_button(
                    label="💾 Simpan Dokumen Ke Perangkat (PDF)",
                    data=f,
                    file_name=file_path,
                    mime="application/pdf",
                    use_container_width=True
                )
        except:
            st.error("Gagal memuat file unduhan.")

    st.divider()
    st.caption("© 2026 Petani_Abies AI - Sistem Klasifikasi Benih Ikan Terverifikasi")
