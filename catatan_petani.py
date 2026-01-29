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
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        .bio-card {
            background-color: #F0FDFA;
            padding: 20px;
            border-radius: 12px;
            border-left: 8px solid #14B8A6;
            margin-bottom: 20px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.02);
        }
        .observation-box {
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        .img-caption {
            font-size: 14px;
            color: #64748B;
            text-align: center;
            font-style: italic;
            margin-top: 5px;
        }
        </style>
        <div class="farmer-header">
            <h1 style="margin:0; color:white;">👨‍🌾 Catatan & Observasi Lapangan</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">Dokumentasi Wawancara & Pengumpulan Dataset Dataset</p>
        </div>
    """, unsafe_allow_html=True)

    # --- BAGIAN 1: PROFIL NARASUMBER ---
    st.subheader("👤 Profil Narasumber Utama")
    col_bio, col_desc = st.columns([1, 2])
    
    with col_bio:
        # Menggunakan foto profil Pak Heru yang baru
        st.image("profil_pak_heru.png", use_container_width=True)
        st.markdown("<p style='text-align:center; font-weight:bold;'>Bapak Heru</p>", unsafe_allow_html=True)

    with col_desc:
        st.markdown("""
            <div class="bio-card">
                <p style="font-size: 18px; color: #0D9488; font-weight: bold;">Pemilik Toko Barokah, Karanggeneng</p>
                <p>Beliau adalah praktisi berpengalaman yang telah menekuni dunia pembenihan berbagai jenis ikan selama <b>22 tahun</b> (sejak 2004).</p>
                <p>Wawancara dipilih sebagai metode utama karena informasi yang diberikan dianggap sangat <b>valid, akurat, dan efektif</b> berdasarkan pengalaman panjang beliau di lapangan.</p>
                <p><i>"Wawasan beliau mengenai ciri fisik dan faktor lingkungan menjadi dasar utama pemberian label pada dataset kami."</i></p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- BAGIAN 2: METODE & HASIL OBSERVASI ---
    st.subheader("🔍 Metodologi & Dataset")
    
    col_text, col_stats = st.columns([1.5, 1])
    
    with col_text:
        st.markdown("""
        **Langkah Awal Penelitian:**
        Penulis melakukan wawancara langsung dan observasi di objek penelitian untuk memperoleh data primer. 
        
        **Hasil Temuan Lapangan:**
        * Informasi dari Bapak Heru digunakan sebagai tambahan dasar pemberian label kualitas.
        * Penentuan kategori benih juga merujuk pada ciri-ciri morfologi dari **BSN (Badan Standardisasi Nasional)**.
        * Data awal yang diperoleh mencakup variasi benih ikan mas, nener, dan mujair.
        """)

    with col_stats:
        st.markdown("<div class='observation-box'>", unsafe_allow_html=True)
        st.write("📊 **Dataset Terkumpul**")
        st.metric("Kualitas Baik", "1.500 Gambar")
        st.metric("Kurang Sehat", "1.500 Gambar")
        st.markdown("<small>Dataset divalidasi oleh pengalaman ahli</small></div>", unsafe_allow_html=True)

    st.divider()

    # --- BAGIAN 3: GALERI PENELITIAN ---
    st.subheader("📸 Galeri Dokumentasi Lapangan")
    st.write("Contoh foto benih ikan mas yang digunakan dalam penelitian berdasarkan kategori kualitas:")

    c1, c2 = st.columns(2)
    with c1:
        st.image("gambar_lapangan1.jpeg", use_container_width=True)
        st.markdown('<p class="img-caption">Dokumentasi pengambilan sampel dataset (1)</p>', unsafe_allow_html=True)
        
    with c2:
        st.image("gambar_lapangan2.jpeg", use_container_width=True)
        st.markdown('<p class="img-caption">Dokumentasi pengambilan sampel dataset (2)</p>', unsafe_allow_html=True)

    st.info("💡 Semua foto mewakili kategori benih berkualitas baik dan tidak berkualitas berdasarkan pengalaman lapangan dan standar BSN.")
