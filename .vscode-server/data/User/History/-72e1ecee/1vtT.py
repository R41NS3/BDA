import pandas as pd

# Membaca data (misalnya data dalam file CSV)
# Gantilah path ke file CSV jika Anda menyimpannya di disk
data = pd.read_csv('/home/uddin/hasil/hasil_pengolahan.csv')

# Menampilkan data pertama untuk melihat struktur
print(data.head())

# Membuat pivot table berdasarkan kolom yang diinginkan, misalnya berdasarkan 'Image'
pivot_table = pd.pivot_table(
    data,
    values=['R', 'G', 'B', 'H_HSV', 'S_HSV', 'V', 'H_HSV', 'S_HSL', 'V', 'HSL'],
    index=['Image'],  # Anda bisa mengubahnya sesuai dengan kolom yang ingin dikelompokkan
    aggfunc='mean'    # Menghitung rata-rata untuk setiap kategori
)

# Menampilkan pivot table
print(pivot_table)

# Menyimpan hasil pivot table ke file CSV jika diperlukan
pivot_table.to_csv('pivot_table_result.csv')
