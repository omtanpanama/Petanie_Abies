import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st
import pandas as pd
import cv2
from streamlit_gsheets import GSheetsConnection
from lime import lime_image
from skimage.segmentation import mark_boundaries

@st.cache_resource
def load_model_cloud():
    file_id = '1kcCLln1DIDCVyEC_Qw26k8fKu2clLI2f'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_petani_siap.keras'
    if not os.path.exists(output):
        with st.spinner("✨ Menghubungkan ke Cloud AI..."):
            gdown.download(url, output, quiet=False)
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x

def generate_lime_explanation(img, model):
    """
    Menggunakan LIME untuk mendeteksi area fisik ikan secara spesifik.
    """
    # Konversi image ke array untuk LIME
    img_array = np.array(img.resize((224, 224)))
    
    explainer = lime_image.LimeImageExplainer()
    
    # Fungsi prediksi untuk LIME
    def predict_fn(images):
        preds = model.predict(tf.keras.applications.resnet50.preprocess_input(images), verbose=0)
        # ResNet50 kamu mungkin binary (1 output) atau 2 output
        if preds.shape[1] == 1:
            return np.hstack([1-preds, preds]) 
        return preds

    explanation = explainer.explain_instance(
        img_array.astype('double'), 
        predict_fn, 
        top_labels=1, 
        hide_color=0, 
        num_samples=200 # Atur ke 200 agar tetap cepat di Streamlit
    )

    # Ambil area (mask) yang paling berpengaruh terhadap label Kurang Sehat
    temp, mask = explanation.get_image_and_mask(
        explanation.top_labels[0], 
        positive_only=True, 
        num_features=5, 
        hide_rest=False
    )
    
    # Overlay visualisasi
    img_lime = mark_boundaries(temp / 255.0, mask)
    img_lime = (img_lime * 255).astype(np.uint8)

    return img_lime, mask

def get_explanation(label, mask, is_dry=False):
    """
    Menganalisis lokasi mask LIME untuk menentukan jenis kerusakan fisik.
    """
    if label == "KUALITAS BAIK":
        return "Fisik proporsional, simetris, dan sirip lengkap."
    
    reasons = []
    if is_dry:
        reasons.append("Kondisi tubuh pucat atau kering")

    # Analisis lokasi mask (224x224)
    # Mencari titik pusat massa dari mask LIME
    coords = np.argwhere(mask > 0)
    if len(coords) > 0:
        y_center, x_center = coords.mean(axis=0)
        
        # Hitung jarak dari pusat gambar (112, 112)
        dist = np.sqrt((x_center - 112)**2 + (y_center - 112)**2)

        # 1. Cek Area Mata (Biasanya di bagian depan atas)
        if y_center < 90 and x_center > 130:
            reasons.append("Kelainan pada area mata")
        
        # 2. Cek Area Sirip/Ekor (Jauh dari pusat)
        if dist > 50:
            reasons.append("Sirip tidak utuh atau ada kerusakan")
            
        # 3. Cek Area Tubuh (Dekat pusat)
        if dist <= 75:
            reasons.append("Bentuk tubuh kurang proporsional")

    if not reasons:
        return "Terdeteksi adanya kelainan fisik pada benih."
            
    return ", ".join(reasons)

def save_to_google_sheets(new_data_df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
    except Exception as e:
        st.error(f"Gagal simpan ke Sheets: {e}")
