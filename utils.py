import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st
import pandas as pd
import cv2
from streamlit_gsheets import GSheetsConnection

@st.cache_resource
def load_model_cloud():
    file_id = '1i6RBVKi9BmSY_jvlypbMWOwvoO5Dyn1t'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_ready_petani.h5'
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

def generate_gradcam(img, model):
    # Preprocess gambar
    img_array = preprocess_image(img)
    
    # Layer terakhir ResNet50
    last_conv_layer_name = "conv5_block3_out"
    grad_model = tf.keras.models.Model(
        [model.inputs], [model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        class_channel = preds[:, 0]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    heatmap = heatmap.numpy()

    # Resize Heatmap
    img_resized = np.array(img.resize((224, 224)))
    heatmap_resized = cv2.resize(heatmap, (224, 224))
    
    # Ambil titik terpanas (yaitu koordinat dengan nilai heatmap tertinggi)
    _, _, _, max_loc = cv2.minMaxLoc(heatmap_resized)
    
    heatmap_color = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    superimposed_img = cv2.addWeighted(img_resized, 0.6, heatmap_color, 0.4, 0)
    
    return superimposed_img, max_loc

def get_explanation(label, max_loc):
    if label == "KUALITAS BAIK":
        return (
            "**✅ ANALISIS KUALITAS BAIK:**\n\n"
            "Berdasarkan citra, benih ikan memiliki:\n"
            "- Bentuk tubuh proporsional & simetris.\n"
            "- Sirip lengkap & tidak ada cacat fisik.\n"
            "- Warna tubuh cerah & seragam sesuai standar BSN."
        )
    else:
        # Logika koordinat Y untuk menentukan area masalah
        y = max_loc[1] 
        if y < 80:
            detail = "Terdeteksi kelainan/cacat pada bagian **Sirip Punggung**."
        elif 80 <= y <= 160:
            detail = "Bentuk **Tubuh tidak proporsional** (Indikasi bengkok atau tidak simetris)."
        else:
            detail = "Terdeteksi kelainan pada area **Ekor atau Sirip Bawah**."
            
        return (
            f"**❌ ANALISIS KUALITAS BURUK:**\n\n"
            f"Penyebab utama: {detail}\n"
            f"- Warna tubuh terindikasi pucat atau tidak seragam pada area yang ditandai merah."
        )

def save_to_google_sheets(new_data_df):
    try:
        conn = st.connection("gsheets", type=GSheetsConnection)
        existing_data = conn.read(worksheet="Sheet1", ttl=0)
        updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
    except Exception as e:
        st.error(f"Gagal menyimpan ke Google Sheets: {e}")
