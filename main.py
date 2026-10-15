import customtkinter as ctk
import yt_dlp
import threading
import imageio_ffmpeg
import os
import sys
import math

class MedyaIndiriciApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Medya İndirici")
        self.geometry("740x480")
        self.eval('tk::PlaceWindow . center')
        
        # Set icon
        icon_path = self.resource_path("icon3.ico")
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        # Remove default title bar
        self.overrideredirect(True)
        
        # Transparent window for custom rounded corners effect
        self.configure(fg_color="#0a0a0a") # Deep dark for shadow effect
        
        # Main background frame (Warm Dark)
        self.bg_frame = ctk.CTkFrame(self, fg_color="#181715", corner_radius=0, border_width=1, border_color="#2b2823")
        self.bg_frame.pack(fill="both", expand=True)

        # Create a Canvas for elegant background animations
        # We put it first so it stays in the background
        self.canvas = ctk.CTkCanvas(self.bg_frame, width=740, height=480, bg="#181715", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        # Title Bar (Elegant)
        self.title_bar = ctk.CTkFrame(self.bg_frame, fg_color="transparent", height=40)
        self.title_bar.pack(fill="x", padx=10, pady=(5, 0))
        self.title_bar.bind("<ButtonPress-1>", self.start_move)
        self.title_bar.bind("<ButtonRelease-1>", self.stop_move)
        self.title_bar.bind("<B1-Motion>", self.do_move)

        self.title_label = ctk.CTkLabel(self.title_bar, text="MEDYA ATÖLYESİ", font=ctk.CTkFont(family="Georgia", size=14, weight="bold"), text_color="#C89B66")
        self.title_label.pack(side="left", padx=10)
        
        self.btn_frame = ctk.CTkFrame(self.title_bar, fg_color="transparent")
        self.btn_frame.pack(side="right")
        
        self.min_btn = ctk.CTkButton(self.btn_frame, text="—", width=35, height=35, fg_color="transparent", hover_color="#2b2823", text_color="#EAE6D5", font=ctk.CTkFont(size=14), command=self.minimize_app)
        self.min_btn.pack(side="left")

        self.close_btn = ctk.CTkButton(self.btn_frame, text="✕", width=35, height=35, fg_color="transparent", hover_color="#8c3a3a", text_color="#EAE6D5", font=ctk.CTkFont(size=14), command=self.close_app)
        self.close_btn.pack(side="left")
        
        # Content Frame
        self.content_frame = ctk.CTkFrame(self.bg_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=60, pady=30)

        # Description
        self.desc_label = ctk.CTkLabel(self.content_frame, text="Medyayı çalışma masasına bırakın.", 
                                       font=ctk.CTkFont(family="Segoe UI", size=26, weight="bold"), text_color="#EAE6D5")
        self.desc_label.pack(pady=(20, 5), anchor="w")
        
        self.sub_desc = ctk.CTkLabel(self.content_frame, text="İstediğiniz videonun veya müziğin bağlantısını yapıştırın,\nbiz sizin için onu en temiz formatında hazırlayalım.", 
                                       font=ctk.CTkFont(size=13), text_color="#8A8679", justify="left")
        self.sub_desc.pack(pady=(0, 30), anchor="w")

        # URL Input
        self.url_var = ctk.StringVar()
        self.url_entry = ctk.CTkEntry(self.content_frame, textvariable=self.url_var, placeholder_text="Bağlantıyı buraya yapıştırın...", 
                                      height=50, font=ctk.CTkFont(size=14), corner_radius=6, 
                                      fg_color="#1E1C1A", border_color="#3A362D", border_width=1, text_color="#EAE6D5")
        self.url_entry.pack(fill="x", pady=(0, 20))
        
        # Bind Enter key to download
        self.url_entry.bind("<Return>", lambda event: self.start_download())
        self.bind("<Return>", lambda event: self.start_download())
        
        # Options Frame
        self.options_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.options_frame.pack(fill="x", pady=(0, 20))

        self.format_var = ctk.StringVar(value="Video (MP4)")
        self.radio_video = ctk.CTkRadioButton(self.options_frame, text="Video (MP4)", variable=self.format_var, value="Video (MP4)", 
                                              font=ctk.CTkFont(size=13), text_color="#D1CDBF", fg_color="#C89B66", hover_color="#B58B5C", border_color="#5A554A")
        self.radio_video.pack(side="left", padx=(0, 20))

        self.radio_audio = ctk.CTkRadioButton(self.options_frame, text="Sadece Ses (MP3)", variable=self.format_var, value="Audio (MP3)",
                                              font=ctk.CTkFont(size=13), text_color="#D1CDBF", fg_color="#C89B66", hover_color="#B58B5C", border_color="#5A554A")
        self.radio_audio.pack(side="left")

        # Download Button
        self.download_btn = ctk.CTkButton(self.content_frame, text="İNDİRMEYİ BAŞLAT", height=45, width=180, font=ctk.CTkFont(size=13, weight="bold"),
                                          fg_color="#C89B66", text_color="#181715", hover_color="#B58B5C", corner_radius=6, command=self.start_download)
        self.download_btn.pack(anchor="w", pady=(10, 15))

        # Progress elements
        self.progress_bar = ctk.CTkProgressBar(self.content_frame, height=4, corner_radius=0, fg_color="#2b2823", progress_color="#C89B66")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(10, 5))
        self.progress_bar.pack_forget() # Hide initially

        self.status_label = ctk.CTkLabel(self.content_frame, text="", font=ctk.CTkFont(size=12), text_color="#8A8679")
        self.status_label.pack(anchor="w", pady=5)

        # Variables
        self._drag_start_x = 0
        self._drag_start_y = 0
        
        self.bind("<Map>", self.on_map)
        self.downloading = False
        self.angle = 0
        
        # Start animations
        self.attributes('-alpha', 0.0)
        self.fade_in()
        self.animate_canvas()
        
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def animate_canvas(self):
        self.canvas.delete("all")
        # Draw a beautiful rotating elegant pattern on the right side
        cx, cy = 600, 200
        r1, r2, r3 = 130, 155, 180
        
        self.angle += 0.005
        
        # Inner dashed circle
        for i in range(12):
            a = self.angle + (i * math.pi / 6)
            x1 = cx + math.cos(a) * r1
            y1 = cy + math.sin(a) * r1
            x2 = cx + math.cos(a + 0.2) * r1
            y2 = cy + math.sin(a + 0.2) * r1
            self.canvas.create_line(x1, y1, x2, y2, fill="#3A362D", width=1)
            
        # Outer dashed circle (counter rotating)
        for i in range(8):
            a = -self.angle * 1.5 + (i * math.pi / 4)
            x1 = cx + math.cos(a) * r2
            y1 = cy + math.sin(a) * r2
            x2 = cx + math.cos(a + 0.3) * r2
            y2 = cy + math.sin(a + 0.3) * r2
            self.canvas.create_line(x1, y1, x2, y2, fill="#4A453A", width=1)

        # Subtle glowing accent dot
        x_g = cx + math.cos(self.angle * 0.8) * r3
        y_g = cy + math.sin(self.angle * 0.8) * r3
        self.canvas.create_oval(x_g-2, y_g-2, x_g+2, y_g+2, fill="#C89B66", outline="")
        
        # A thin geometric shape mimicking a paper/canvas in the background
        self.canvas.create_rectangle(cx-60, cy-80, cx+60, cy+80, outline="#2b2823", width=1)
        self.canvas.create_line(cx+40, cy-80, cx+60, cy-60, fill="#2b2823", width=1)

        self.after(30, self.animate_canvas)
        
    def start_move(self, event):
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def stop_move(self, event):
        pass

    def do_move(self, event):
        x = self.winfo_x() + (event.x_root - self._drag_start_x)
        y = self.winfo_y() + (event.y_root - self._drag_start_y)
        self.geometry(f"+{x}+{y}")
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root

    def minimize_app(self):
        self.overrideredirect(False)
        self.iconify()

    def on_map(self, event):
        if self.state() == 'normal' and not self.overrideredirect():
            self.overrideredirect(True)

    def fade_in(self):
        alpha = self.attributes('-alpha')
        if alpha < 1.0:
            self.attributes('-alpha', alpha + 0.05)
            self.after(20, self.fade_in)

    def fade_out_and_close(self):
        alpha = self.attributes('-alpha')
        if alpha > 0.0:
            self.attributes('-alpha', alpha - 0.05)
            self.after(15, self.fade_out_and_close)
        else:
            self.destroy()

    def close_app(self):
        if self.downloading:
            self.status_label.configure(text="İşlem devam ederken kapatılamaz, lütfen bekleyin.", text_color="#A85A5A")
            return
        self.fade_out_and_close()

    def my_hook(self, d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','').strip()
            import re
            p = re.sub(r'\x1b\[[0-9;]*m', '', p)
            try:
                percent = float(p) / 100.0
                self.progress_bar.set(percent)
                speed = d.get('_speed_str', 'Bilinmiyor')
                eta = d.get('_eta_str', 'Bilinmiyor')
                speed = re.sub(r'\x1b\[[0-9;]*m', '', speed)
                eta = re.sub(r'\x1b\[[0-9;]*m', '', eta)
                self.status_label.configure(text=f"İndiriliyor: %{p} | Hız: {speed} | Kalan: {eta}", text_color="#C89B66")
            except Exception as e:
                pass
        elif d['status'] == 'finished':
            self.status_label.configure(text="İndirme tamamlandı, dosya hazırlanıyor...", text_color="#C89B66")
            self.progress_bar.set(1.0)

    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            self.status_label.configure(text="Lütfen geçerli bir bağlantı girin.", text_color="#A85A5A")
            return

        self.downloading = True
        self.download_btn.configure(state="disabled", text="HAZIRLANIYOR...", fg_color="#5A554A")
        self.progress_bar.pack(fill="x", pady=(10, 5))
        self.progress_bar.set(0)
        self.status_label.configure(text="Bağlantı kuruluyor...", text_color="#8A8679")
        
        thread = threading.Thread(target=self.download_thread, args=(url,))
        thread.start()

    def download_thread(self, url):
        try:
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            is_audio = (self.format_var.get() == "Audio (MP3)")
            
            ydl_opts = {
                'outtmpl': os.path.join(desktop_path, '%(title)s.%(ext)s'),
                'progress_hooks': [self.my_hook],
                'ffmpeg_location': ffmpeg_path,
                'quiet': True,
                'no_warnings': True,
                'nocheckcertificate': True,
                'noplaylist': True,
                'concurrent_fragment_downloads': 10,
                'restrictfilenames': True
            }

            if is_audio:
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ydl_opts['postprocessor_args'] = {
                    'default': [
                        '-codec:a', 'libmp3lame',
                        '-ar', '44100',
                        '-ac', '2',
                        '-b:a', '192k',
                        '-joint_stereo', '1',
                        '-id3v2_version', '3',
                        '-map_metadata', '-1'
                    ]
                }
            else:
                ydl_opts['format'] = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.status_label.configure(text="Dosya başarıyla masanıza bırakıldı.", text_color="#87A878")
            
        except Exception as e:
            self.status_label.configure(text=f"Hata oluştu, bağlantıyı kontrol edin.", text_color="#A85A5A")
            print(e)
            
        finally:
            self.downloading = False
            self.download_btn.configure(state="normal", text="İNDİRMEYİ BAŞLAT", fg_color="#C89B66")
            self.after(6000, self.reset_ui)

    def reset_ui(self):
        if not self.downloading:
            self.progress_bar.pack_forget()
            self.status_label.configure(text="")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = MedyaIndiriciApp()
    app.mainloop()
