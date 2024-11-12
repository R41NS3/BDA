import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Path file hasil_pengolahan.csv
file_path = '/home/uddin/hasil/hasil_pengolahan.csv'

# Memuat data
df = pd.read_csv(file_path)

# Menampilkan beberapa baris pertama data
print("Preview data:")
print(df.head())

# Menampilkan statistik deskriptif
print("\nStatistik deskriptif:")
print(df.describe())

# Visualisasi distribusi nilai R, G, B
plt.figure(figsize=(14, 6))
sns.histplot(df['R'], kde=True, color='red', label='R', bins=30)
sns.histplot(df['G'], kde=True, color='green', label='G', bins=30)
sns.histplot(df['B'], kde=True, color='blue', label='B', bins=30)
plt.title('Distribusi Nilai R, G, B')
plt.xlabel('Nilai')
plt.ylabel('Frekuensi')
plt.legend()
plt.show()

# Visualisasi distribusi nilai H, S, V (HSV)
plt.figure(figsize=(14, 6))
sns.histplot(df['H_HSV'], kde=True, color='purple', label='H_HSV', bins=30)
sns.histplot(df['S_HSV'], kde=True, color='orange', label='S_HSV', bins=30)
sns.histplot(df['V'], kde=True, color='yellow', label='V', bins=30)
plt.title('Distribusi Nilai H, S, V (HSV)')
plt.xlabel('Nilai')
plt.ylabel('Frekuensi')
plt.legend()
plt.show()

# Visualisasi distribusi nilai H, S, L (HSL)
plt.figure(figsize=(14, 6))
sns.histplot(df['H_HSL'], kde=True, color='purple', label='H_HSL', bins=30)
sns.histplot(df['S_HSL'], kde=True, color='orange', label='S_HSL', bins=30)
sns.histplot(df['L'], kde=True, color='pink', label='L', bins=30)
plt.title('Distribusi Nilai H, S, L (HSL)')
plt.xlabel('Nilai')
plt.ylabel('Frekuensi')
plt.legend()
plt.show()

# Menampilkan korelasi antar variabel
plt.figure(figsize=(12, 10))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriks Korelasi Antar Variabel')
plt.show()
