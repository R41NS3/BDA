import pandas as pd

# Membaca data (misalnya data dalam file CSV)
# Gantilah path ke file CSV jika Anda menyimpannya di disk
data = pd.read_csv('/home/uddin/hasil/hasil_pengolahan.csv')

# Menampilkan data pertama untuk melihat struktur
print(data.head())

# Memastikan bahwa semua kolom yang digunakan ada dalam DataFrame
required_columns = ['R', 'G', 'B', 'H_HSV', 'S_HSV', 'V', 'S_HSL', 'HSL', 'Image']
missing_columns = [col for col in required_columns if col not in data.columns]

if missing_columns:
    print(f"Kolom berikut tidak ditemukan dalam data: {', '.join(missing_columns)}")
else:
    # Membuat pivot table berdasarkan kolom yang diinginkan
    pivot_table = pd.pivot_table(
        data,
        values=['R', 'G', 'B', 'H_HSV', 'S_HSV', 'V', 'S_HSL', 'HSL'],
        index=['Image'],  # Anda bisa mengubahnya sesuai dengan kolom yang ingin dikelompokkan
        aggfunc='mean'    # Menghitung rata-rata untuk setiap kategori
    )

    # Menampilkan pivot table
    print(pivot_table)

    # Menyimpan hasil pivot table ke file CSV jika diperlukan
    pivot_table.to_csv('/home/uddin/hasil/pivot_table_result.csv')
