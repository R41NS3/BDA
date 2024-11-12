import cv2
import pandas as pd
import numpy as np
import os

# Direktori tempat gambar disimpan
directory = '/home/uddin/downloaded_files'
output_directory = '/home/uddin/hasil'

# Menentukan ambang batas ukuran file (dalam MB)
size_threshold_mb = 5  # Ubah sesuai kebutuhan
size_threshold_bytes = size_threshold_mb * 1024 * 1024

# Mencari gambar berukuran besar dalam direktori
selected_images = []
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    if os.path.isfile(filepath) and filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
        file_size = os.path.getsize(filepath)
        if file_size > size_threshold_bytes:
            selected_images.append(filepath)

# Mengecek apakah ada gambar yang terdeteksi
if not selected_images:
    print("Tidak ada gambar yang melebihi ukuran ambang batas.")
else:
    for image_path in selected_images:
        print(f"Memproses gambar: {image_path}")
        
        # Image processing: Load image
        image = cv2.imread(image_path)

        # Ekstrak to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Ekstrak to HSV
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Ekstrak to HSL
        image_hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

        # Create dataframe
        data = {
            'R': image_rgb[:, :, 0].flatten(),
            'G': image_rgb[:, :, 1].flatten(),
            'B': image_rgb[:, :, 2].flatten(),
            'H_HSV': image_hsv[:, :, 0].flatten(),
            'S_HSV': image_hsv[:, :, 1].flatten(),
            'V': image_hsv[:, :, 2].flatten(),
            'H_HSL': image_hsl[:, :, 0].flatten(),
            'S_HSL': image_hsl[:, :, 1].flatten(),
            'L': image_hsl[:, :, 2].flatten(),
        }

        df = pd.DataFrame(data)

        # Analytic the pivot table (mean of each column)
        pivot_table = df.mean()

        # Simpan hasil ke file CSV
        output_path = os.path.join(output_directory, 'hasil_pengolahan.csv')
        pivot_table.to_csv(output_path, header=True)

        print(f"Hasil disimpan di: {output_path}")
