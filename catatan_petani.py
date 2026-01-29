import streamlit as st

def render_catatan_petani():
    # Header dengan Background Warna Hijau Alam (Petani)
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
        .observation-box {
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #E5E7EB;
            border-radius: 10px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        </style>
        <div class="farmer-header">
            <h1 style="margin:0; color:white;">👨‍🌾 Catatan & Observasi Lapangan</h1>
            <p style="margin:5px 0 0 0; opacity: 0.9;">Dokumentasi Pengumpulan Dataset & Wawancara Pakar Lokal</p>
        </div>
    """, unsafe_allow_html=True)

    # --- BAGIAN 1: PROFIL NARASUMBER ---
    st.subheader("👤 Profil Narasumber Utama")
    col_bio, col_desc = st.columns([1, 2])
    
    with col_bio:
        # Ganti dengan path foto Bapak Heru jika ada, atau gunakan icon
        st.markdown("""
            <div style="text-align: center; padding: 20px; background: #f3f4f6; border-radius: 50%;">
                <span style="font-size: 100px;">👨‍🌾</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'><b>Bapak Heru</b></p>", unsafe_allow_html=True)

    with col_desc:
        st.markdown("""
            <div class="bio-card">
                <p><b>Pemilik Toko Barokah, Karanggeneng</b></p>
                <p>Beliau adalah praktisi pembenihan ikan dengan pengalaman lebih dari <b>22 tahun</b> (sejak 2004). 
                Keahliannya mencakup budidaya ikan mas, nener, dan mujair.</p>
                <p><i>"Pengalaman lapangan Bapak Heru menjadi kunci dalam penentuan label kualitas dataset Petani_Abies."</i></p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- BAGIAN 2: METODE & HASIL OBSERVASI ---
    st.subheader("🔍 Metodologi Pengumpulan Data")
    
    col_text, col_stats = st.columns([1.5, 1])
    
    with col_text:
        st.markdown("""
        Penelitian ini menggunakan metode **Wawancara Langsung** dan **Observasi Lapangan**. 
        Informasi dari praktisi dikombinasikan dengan standar **BSN (Badan Standardisasi Nasional)** untuk memastikan akurasi label pada model AI.
        
        **Poin Utama Wawancara:**
        * Identifikasi ciri fisik benih unggul vs benih cacat.
        * Pengaruh faktor lingkungan terhadap kesehatan benih.
        * Validasi kategori dataset berdasarkan kebiasaan petani lokal.
        """)

    with col_stats:
        st.markdown("<div class='observation-box'>", unsafe_allow_html=True)
        st.write("**Total Dataset Terkumpul:**")
        st.metric("Kualitas Baik", "1.500 Gambar", delta="Valid")
        st.metric("Kurang Sehat", "1.500 Gambar", delta="Valid", delta_color="inverse")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()

    # --- BAGIAN 3: GALERI PENELITIAN ---
    st.subheader("📸 Galeri Dokumentasi Lapangan")
    st.write("Representasi visual benih ikan mas yang diambil selama proses penelitian:")

    # Ganti 'gambar_penelitian_1.jpg' dengan file asli di GitHub kamu
    c1, c2 = st.columns(2)
    with c1:
        # Masukkan gambar pas penelitian di sini
        st.image("https://via.placeholder.com/500x350?text=Foto+Penelitian+1", 
                 caption="Proses Pengambilan Sampel di Toko Barokah", use_container_width=True)
    with c2:
        st.image("https://via.placeholder.com/500x350?text=Foto+Penelitian+2", 
                 caption="Klasifikasi Fisik Benih Bersama Bapak Heru", use_container_width=True)

    st.info("💡 Semua foto diambil menggunakan pencahayaan alami untuk menyesuaikan kondisi lapangan petani.")
