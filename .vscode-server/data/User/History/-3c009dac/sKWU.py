import os
import io
import time
import pandas as pd
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError

# Menambahkan timestamp waktu tanpa tanda - atau :
def get_timestamp():
    return time.strftime("%d%m%Y%H%M")

# Fungsi untuk menginisiasi Google Drive API dengan API key
def authenticate_drive_api_with_api_key(api_key):
    service = build('drive', 'v3', developerKey=api_key)
    return service

# Fungsi untuk mendapatkan semua file di folder Google Drive
def list_files_in_folder(service, folder_id):
    try:
        results = service.files().list(
            q=f"'{folder_id}' in parents",
            pageSize=1000, fields="files(id, name, mimeType)").execute()
        return results.get('files', [])
    except HttpError as e:
        print(f"HttpError saat mencoba mendapatkan file dalam folder {folder_id}: {e}")
        return []

# Fungsi untuk mengunduh file dan menyimpannya ke disk
def download_file(service, file_id, file_name, file_url):
    try:
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Progress download {file_name}: {int(status.progress() * 100)}%")
        
        # Simpan file ke disk
        file_stream.seek(0)  # Reset posisi pointer ke awal
        file_path = os.path.join('downloaded_files', file_name)
        with open(file_path, 'wb') as f:
            f.write(file_stream.read())
        print(f"File {file_name} telah diunduh dan disimpan.")
        
        return file_path
    except HttpError as e:
        print(f"HttpError saat mencoba mengunduh {file_name}: {e}")
        return None

# Fungsi untuk mengunduh file CSV dan menggabungkan menjadi satu DataFrame
def download_and_append_csv(service, file_id, file_name, combined_df, file_url):
    try:
        request = service.files().get_media(fileId=file_id)
        file_stream = io.BytesIO()
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Progress download CSV: {int(status.progress() * 100)}%")
        
        # Membaca CSV dari memori menggunakan pandas
        file_stream.seek(0)  # Reset posisi pointer ke awal
        try:
            df = pd.read_csv(file_stream)
            # Tambahkan kolom timestamp dan URL
            timestamp = get_timestamp()
            df['timestamp'] = timestamp
            df['file_url'] = file_url
            # Tambahkan file ke DataFrame gabungan
            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f"File CSV {file_name} dengan timestamp {timestamp} dan URL {file_url} telah ditambahkan ke DataFrame gabungan.")
        except Exception as e:
            print(f"Error membaca CSV {file_name}: {e}")
    except HttpError as e:
        print(f"HttpError saat mencoba mengunduh CSV {file_name}: {e}")
    return combined_df

# Fungsi untuk mengonversi metadata file menjadi DataFrame
def file_metadata_to_df(file_name, file_type, file_url=None):
    # Membuat DataFrame dari metadata file
    df = pd.DataFrame({
        'timestamp': [get_timestamp()],
        'file_name': [file_name],
        'file_type': [file_type],
        'file_url': [file_url] if file_url else [None]
    })
    return df

# Fungsi untuk melakukan download file dari folder dan subfolder
def process_folder(service, folder_id, combined_df):
    # Dapatkan list file di dalam folder
    files = list_files_in_folder(service, folder_id)

    for file in files:
        # Ambil URL file di Google Drive
        file_url = f"https://drive.google.com/uc?id={file['id']}"
        
        # Jika file adalah folder, lakukan rekursif
        if file['mimeType'] == 'application/vnd.google-apps.folder':
            print(f"Masuk ke dalam folder: {file['name']}")
            combined_df = process_folder(service, file['id'], combined_df)  # Rekursif ke subfolder
        # Jika file adalah CSV, tampilkan kolom dan gabungkan ke DataFrame
        elif file['mimeType'] == 'text/csv':
            print(f"Menampilkan kolom file CSV: {file['name']}")
            combined_df = download_and_append_csv(service, file['id'], file['name'], combined_df, file_url)
        # Jika file adalah XLSX, unduh file
        elif file['mimeType'] == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            print(f"Menampilkan kolom file XLSX: {file['name']}")
            file_path = download_file(service, file['id'], file['name'], file_url)
            if file_path:
                df = file_metadata_to_df(file['name'], 'XLSX', file_url)
                combined_df = pd.concat([combined_df, df], ignore_index=True)
        # Jika file adalah JPG, PNG, HEIC, dll, unduh file
        elif file['mimeType'] in ['image/jpeg', 'image/png', 'image/heic']:
            print(f"Menampilkan kolom file gambar: {file['name']}")
            file_path = download_file(service, file['id'], file['name'], file_url)
            if file_path:
                df = file_metadata_to_df(file['name'], 'Image', file_url)
                combined_df = pd.concat([combined_df, df], ignore_index=True)
        # Jika file adalah video atau file lain, unduh file
        elif file['mimeType'] in ['video/mp4']:
            print(f"Menampilkan kolom file video: {file['name']}")
            file_path = download_file(service, file['id'], file['name'], file_url)
            if file_path:
                df = file_metadata_to_df(file['name'], 'Video', file_url)
                combined_df = pd.concat([combined_df, df], ignore_index=True)
        # Untuk file lain, abaikan
        else:
            print(f"Melewatkan file: {file['name']} (bukan CSV, XLSX, gambar, atau video)")
    
    return combined_df

def main():
    folder_id = '119PrV1WskzGGh29eo0RPziQ_N4IOl0Zz'  # ID folder
    api_key = 'AIzaSyCkTB6RNuZQ0rkoun8lC9a9JP4rSMn84Vk'  # API key Anda
    service = authenticate_drive_api_with_api_key(api_key)  

    # Pastikan folder 'downloaded_files' ada
    if not os.path.exists('downloaded_files'):
        os.makedirs('downloaded_files')
    
    # DataFrame gabungan
    combined_df = pd.DataFrame()
    
    # Memproses folder  (dan subfoldernya secara rekursif)
    combined_df = process_folder(service, folder_id, combined_df)
    
    # Menyimpan DataFrame gabungan ke dalam file CSV
    if not combined_df.empty:
        combined_df.to_csv('file3.csv', index=False)
        print("Semua file telah digabungkan dan disimpan ke file.csv")
    else:
        print("Tidak ada file yang ditemukan untuk digabungkan.")

if __name__ == '__main__':
    main()
