import tkinter as tk
from tkinter import scrolledtext, messagebox
import os
import pickle
import yt_dlp
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def download_video(url, output_dir):
    ydl_opts = {'format': 'mp4', 'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s')}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_filename = ydl.prepare_filename(info_dict)
    return video_filename

def authenticate_youtube():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

def upload_video(youtube, video_path, title, description, tags):
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request_body = {
        'snippet': {'title': title, 'description': description, 'tags': tags, 'categoryId': '22'},
        'status': {'privacyStatus': 'public'}
    }
    request = youtube.videos().insert(part='snippet,status', body=request_body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()

    return response

def start_upload():
    links = link_text.get("1.0", tk.END).strip().splitlines()
    title = title_entry.get()
    description = desc_entry.get("1.0", tk.END).strip()
    tags = tags_entry.get().split(',')

    if not links or not title:
        messagebox.showerror("Hata", "Linkler ve başlık alanları zorunludur!")
        return

    output_dir = 'videos'
    os.makedirs(output_dir, exist_ok=True)

    youtube = authenticate_youtube()

    for url in links:
        try:
            video_file = download_video(url, output_dir)
            upload_video(youtube, video_file, title, description, tags)
            messagebox.showinfo("Başarılı", f"Yüklendi: {title}")
            os.remove(video_file)
        except Exception as e:
            messagebox.showerror("Hata", str(e))

app = tk.Tk()
app.title("TikTok → YouTube Botu")
app.geometry('600x700')

tk.Label(app, text="TikTok Video Linkleri (Her satıra bir link):").pack(pady=5)
link_text = scrolledtext.ScrolledText(app, height=10)
link_text.pack(padx=10, pady=5)

tk.Label(app, text="YouTube Başlığı:").pack(pady=5)
title_entry = tk.Entry(app, width=60)
title_entry.pack(pady=5)

tk.Label(app, text="YouTube Açıklaması:").pack(pady=5)
desc_entry = scrolledtext.ScrolledText(app, height=5)
desc_entry.pack(padx=10, pady=5)

tk.Label(app, text="YouTube Tagleri (virgülle ayır):").pack(pady=5)
tags_entry = tk.Entry(app, width=60)
tags_entry.pack(pady=5)

tk.Button(app, text="Videoları İndir ve YouTube'a Yükle", command=start_upload, bg="green", fg="white", width=40, height=2).pack(pady=20)

app.mainloop()
