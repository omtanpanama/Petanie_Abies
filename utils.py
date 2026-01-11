import tensorflow as tf
import os
import gdown
import streamlit as st

@st.cache_resource
def load_model_cloud():
    # ID File dari Google Drive Anda
    file_id = '1i6RBVKi9BmSY_jvlypbMWOwvoO5Dyn1t'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_ready_petani.h5'
    
    # Cek apakah file sudah ada, jika belum download
    if not os.path.exists(output):
        try:
            with st.spinner("✨ Menghubungkan ke Otak AI Petani_Abies..."):
                gdown.download(url, output, quiet=False)
        except Exception as e:
            st.error(f"Gagal mengunduh model: {e}")
            return None
            
    # Load model tanpa kompilasi agar lebih cepat
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    """Fungsi untuk memproses gambar agar sesuai input model ResNet50"""
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x
