import streamlit as st

def render_catatan_petani():
    # CSS Custom untuk estetika Dashboard
    st.markdown("""
        <style>
        .farmer-header {
            background: linear-gradient(90deg, #115E59 0%, #2DD4BF 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: center;
            margin-bottom: 25px;
        }
        .bio-card {
            background-color: #F0FDFA;
            padding: 20px;
            border-radius: 12px;
            border-left: 8px solid #14B8A6;
            margin-bottom: 20px;
        }
        </style>
        <div class="farmer-header">
            <h1 style="margin:0; color:white;">👨‍🌾 Catatan & Observasi Lapangan</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">Dokumentasi Wawancara & Pengumpulan Dataset</p>
        </div>
    """, unsafe_allow_html=True)

    # --- BAGIAN 1: PROFIL NARASUMBER ---
    st.subheader("👤 Profil Narasumber Utama")
    col_bio, col_desc = st.columns([1, 2])
    
    with col_bio:
        # PENTING: Gunakan try-except agar aplikasi tidak error jika file telat load
        try:
            st.image("profil_pak_heru.png", use_container_width=True)
            st.markdown("<p style='text-align:center; font-weight:bold;'>Bapak Heru</p>", unsafe_allow_html=True)
        except:
            st.error("Gagal memuat foto profil.")

    with col_desc:
        st.markdown("""
            <div class="bio-card">
                <p style="font-size: 18px; color: #0D9488; font-weight: bold;">Pemilik Toko Barokah, Karanggeneng</p>
                <p>Beliau adalah praktisi berpengalaman yang telah menekuni dunia pembenihan ikan selama <b>22 tahun</b> (sejak 2004).</p>
                <p>Wawancara langsung dipilih karena dianggap sangat <b>valid, akurat, dan efektif</b> untuk memperoleh informasi dari ahli lapangan.</p>
                <p><i>"Pengalaman panjang Bapak Heru menjadi kunci dalam penentuan label kualitas dataset Petani_Abies."</i></p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- BAGIAN 2: METODE & DATASET ---
    st.subheader("🔍 Metodologi & Hasil Data")
    
    col_text, col_stats = st.columns([1.5, 1])
    
    with col_text:
        st.markdown("""
        **Proses Penelitian:**
        Penulis menggunakan metode wawancara langsung kepada pembudidaya sebagai objek penelitian. 
        Informasi ini digunakan sebagai dasar pemberian label kualitas pada dataset.
        
        **Kategori Dataset:**
        Label kualitas ditentukan berdasarkan ciri-ciri morfologi dari **BSN (Badan Standardisasi Nasional)** dan validasi dari pengalaman Bapak Heru.
        """)

    with col_stats:
        st.markdown("<div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; text-align: center;'>", unsafe_allow_html=True)
        st.write("📊 **Total Dataset**")
        st.metric("Kualitas Baik", "1.500 Gambar") #
        st.metric("Kurang Sehat", "1.500 Gambar") #
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # --- BAGIAN 3: GALERI LAPANGAN ---
    st.subheader("📸 Galeri Dokumentasi Lapangan")
    st.write("Foto benih ikan mas yang digunakan dalam penelitian berdasarkan kategori kualitas:")

    c1, c2 = st.columns(2)
    with c1:
        try:
            st.image("gambar_lapangan1.jpeg", use_container_width=True)
            st.caption("Dokumentasi Pengambilan Sampel Dataset (1)")
        except:
            st.warning("Foto lapangan 1 sedang dimuat...")
            
    with c2:
        try:
            st.image("gambar_lapangan2.jpeg", use_container_width=True)
            st.caption("Dokumentasi Pengambilan Sampel Dataset (2)")
        except:
            st.warning("Foto lapangan 2 sedang dimuat...")
