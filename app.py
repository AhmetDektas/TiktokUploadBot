import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import pickle
import threading
import time
import requests
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_script_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

def download_video(url, output_folder):
    api_url = 'https://tikwm.com/api/'
    params = {'url': url}
    
   
    try:
        response = requests.get(api_url, params=params, timeout=15).json()
    except requests.RequestException as e:
        raise Exception(f"API Bağlantı Hatası: {e}")

    if response.get('code') != 0:
        raise Exception('Video bulunamadı veya gizli. URL\'yi kontrol edin.')

    video_url = response['data']['play']
    video_bytes = requests.get(video_url, timeout=30).content

    
    file_name = f"video_{int(time.time())}.mp4"
    video_filename = os.path.join(output_folder, file_name)

    with open(video_filename, 'wb') as file:
        file.write(video_bytes)

    return video_filename

def authenticate_youtube():
    creds = None
    token_path = get_script_path("token.pickle")
    secrets_path = get_script_path("client_secrets.json")

    if not os.path.exists(secrets_path):
        raise FileNotFoundError("client_secrets.json dosyası bulunamadı! Lütfen proje klasörüne ekleyin.")

    if os.path.exists(token_path):
        with open(token_path, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(secrets_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, video_path, title, description, tags):
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request_body = {
        'snippet': {
            'title': title, 
            'description': description, 
            'tags': tags, 
            'categoryId': '22' 
        },
        'status': {'privacyStatus': 'public'}
    }
    
    request = youtube.videos().insert(part='snippet,status', body=request_body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        
    
    return response

def process_videos():
    links = link_text.get("1.0", tk.END).strip().splitlines()
    title = title_entry.get()
    description = desc_entry.get("1.0", tk.END).strip()
    tags_raw = tags_entry.get()
    tags = [tag.strip() for tag in tags_raw.split(',') if tag.strip()]

    if not links or not title:
        messagebox.showerror("Hata", "Linkler ve başlık alanları zorunludur")
        upload_btn.config(state=tk.NORMAL, text="Videoları İndir ve YouTube'a Yükle")
        return

    output_dir = get_script_path('videos')
    os.makedirs(output_dir, exist_ok=True)

    status_label.config(text="YouTube'a bağlanılıyor.")
    
    try:
        youtube = authenticate_youtube()
    except Exception as e:
        messagebox.showerror("Yetkilendirme Hatası", str(e))
        upload_btn.config(state=tk.NORMAL, text="Videoları İndir ve YouTube'a Yükle")
        status_label.config(text="Hata oluştu.")
        return

    success_count = 0
    
    for i, url in enumerate(links):
        if not url.strip(): continue
        
        try:
            status_label.config(text=f"{i+1}/{len(links)} - Video İndiriliyor...")
            video_file = download_video(url.strip(), output_dir)
            
            status_label.config(text=f"{i+1}/{len(links)} - YouTube'a Yükleniyor...")
            upload_video(youtube, video_file, title, description, tags)
            
            os.remove(video_file) 
            success_count += 1
            
        except Exception as e:
            print(f"Hata ({url}): {e}") 
            
    status_label.config(text=f"İşlem Tamamlandı! ({success_count} video yüklendi)")
    messagebox.showinfo("Başarılı", f"Toplam {success_count} video başarıyla işlendi.")
    
    
    upload_btn.config(state=tk.NORMAL, text="Videoları İndir ve YouTube'a Yükle")

def start_thread():
    upload_btn.config(state=tk.DISABLED, text="İşlem Sürüyor...")
    threading.Thread(target=process_videos, daemon=True).start()

# --- GUI ---
app = tk.Tk()
app.title("TikTok → YouTube Botu")
app.geometry('600x750')

tk.Label(app, text="TikTok Video Linkleri (Her satıra bir link):", font=("Arial", 10, "bold")).pack(pady=(10, 5))
link_text = scrolledtext.ScrolledText(app, height=8)
link_text.pack(padx=10, pady=5)

tk.Label(app, text="YouTube Başlığı:", font=("Arial", 10, "bold")).pack(pady=5)
title_entry = tk.Entry(app, width=70)
title_entry.pack(pady=5)

tk.Label(app, text="YouTube Açıklaması:", font=("Arial", 10, "bold")).pack(pady=5)
desc_entry = scrolledtext.ScrolledText(app, height=5)
desc_entry.pack(padx=10, pady=5)

tk.Label(app, text="YouTube Etiketleri (virgülle ayır):", font=("Arial", 10, "bold")).pack(pady=5)
tags_entry = tk.Entry(app, width=70)
tags_entry.pack(pady=5)

status_label = tk.Label(app, text="Hazır", fg="blue", font=("Arial", 9, "italic"))
status_label.pack(pady=10)

upload_btn = tk.Button(app, text="Videoları İndir ve YouTube'a Yükle", command=start_thread, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=40, height=2)
upload_btn.pack(pady=10)

app.mainloop()
