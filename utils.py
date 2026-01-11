import tensorflow as tf
import numpy as np
import gdown
import os
import streamlit as st

@st.cache_resource
def load_model_cloud():
    file_id = '1i6RBVKi9BmSY_jvlypbMWOwvoO5Dyn1t'
    url = f'https://drive.google.com/uc?id={file_id}'
    output = 'model_ready_petani.h5'
    if not os.path.exists(output):
        with st.spinner("✨ Menghubungkan ke Otak AI..."):
            gdown.download(url, output, quiet=False)
    return tf.keras.models.load_model(output, compile=False)

def preprocess_image(image):
    # Resize ke 224x224 (Standar ResNet50)
    img = image.resize((224, 224))
    x = tf.keras.preprocessing.image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # Sangat penting: gunakan preprocess_input bawaan ResNet50
    x = tf.keras.applications.resnet50.preprocess_input(x)
    return x
