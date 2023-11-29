import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import pygame
import os
from audio_effects import delay
from configparser import ConfigParser

# Definir variables globales
font_color = ""
bg_color2 = ""
bg_color3 = ""

playUrl = ""
stopUrl = ""
nextUrl = ""
prevUrl = ""
addUrl = ""
deleteUrl = ""

config_path = os.path.join(os.path.dirname(__file__), "config.ini")
icon_path = os.path.join(os.path.dirname(__file__), "images", "icono.png")

def toggle_theme(root):
    current_theme = config.get('Settings', 'theme')
    if current_theme == 'dark':
        new_theme = 'light'
    else:
        new_theme = 'dark'
    config.set('Settings', 'theme', new_theme)
    config.write(open(config_path, 'w'))
    update_theme()
    root.destroy()
    main()

def update_theme():
    global font_color, bg_color2, bg_color3, playUrl, stopUrl, nextUrl, prevUrl, addUrl, deleteUrl
    theme = config.get('Settings', 'theme')
    font_color = config.get(theme, 'font_color')
    bg_color2 = config.get(theme, 'bg_color2')
    bg_color3 = config.get(theme, 'bg_color3')
    playUrl = config.get(theme, 'playUrl')
    stopUrl = config.get(theme, 'stopUrl')
    nextUrl = config.get(theme, 'nextUrl')
    prevUrl = config.get(theme, 'prevUrl')
    addUrl = config.get(theme, 'addUrl')
    deleteUrl = config.get(theme, 'deleteUrl')

# Configuración por defecto
config = ConfigParser()
# config['Settings'] = {'theme': 'light'}

try:
    config.read(config_path)
    update_theme()  
except Exception as e:
    print(f"Error: {e}")
    pass

class ReproductorMusica:
    def __init__(self, root, toggle_theme_callback):
        self.root = root
        self.root.title("Reproductor de Música de Agus")
        self.icon_image = ImageTk.PhotoImage(file=icon_path)
        self.root.iconphoto(True, self.icon_image)
        self.playlist = []
        self.current_track = 0
        self.paused = False
        self.playing = False
        self.play_photo = None
        self.stop_photo = None
        self.next_photo = None
        self.prev_photo = None
        self.current_position = 0
        self.paused_position = 0
        self.delay_enabled = False
        self.init_ui()

    def init_ui(self):
        update_theme()
        self.root.configure(bg=bg_color3)

        self.label = tk.Label(
            self.root, text="Reproductor de Música de Agus", font=("Helvetica", 16), bg=bg_color3, fg=font_color
        )

        self.label.pack(pady=10)
        
        self.buttom = tk.Button(
            self.root, text="Cambiar tema", font=("Helvetica", 12), bg=bg_color3, fg=font_color, command=lambda: toggle_theme(self.root)
        )
        self.buttom.pack(side="top", pady=(0, 0))

        main_frame = tk.Frame(self.root, bg=bg_color3)
        main_frame.pack(fill="both", expand=True)

        playlist_frame = tk.Frame(main_frame, bg=bg_color3)
        playlist_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=10, pady=10)

        self.playlist_label = tk.Label(playlist_frame, text="Lista de Reproducción:", font=("Helvetica", 12), bg=bg_color3, fg=font_color)
        self.playlist_label.pack()

        self.playlist_display = tk.Listbox(playlist_frame, width=40, height=20, bg=bg_color2, fg=font_color, selectbackground=bg_color2, selectforeground=bg_color3)
        self.playlist_display.pack(fill="both", expand=True)

        future_frame = tk.Frame(main_frame, bg=bg_color3)
        future_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=10, pady=10)

        self.delay_button_var = tk.BooleanVar()
        delay_button = tk.Checkbutton(
            future_frame,
            text="Delay",
            variable=self.delay_button_var,
            bg=bg_color3,
            fg=font_color,
            activebackground=bg_color2,
            activeforeground="white",
            command=self.toggle_delay,
        )
        delay_button.pack()

        song_info_frame = tk.Frame(self.root, bg=bg_color3)
        song_info_frame.pack()

        self.filename_label = tk.Label(song_info_frame, text="", font=("Helvetica", 12), bg=bg_color3, fg=font_color)
        self.filename_label.pack()

        control_frame = tk.Frame(self.root, bg=bg_color3)
        control_frame.pack(pady=10)

        self.filename_label = tk.Label(control_frame, text="", font=("Helvetica", 12), bg=bg_color3, fg=font_color)
        self.filename_label.grid(row=0, column=0, columnspan=4, pady=10)

        self.add_photo = ImageTk.PhotoImage(self.resize_image(addUrl, (32, 32)))
        self.delete_photo = ImageTk.PhotoImage(self.resize_image(deleteUrl, (32, 32)))

        self.button_add = tk.Button(
            control_frame, image=self.add_photo, command=self.add_to_playlist, borderwidth=0, bg=bg_color3
        )
        self.button_delete = tk.Button(
            control_frame,
            image=self.delete_photo,
            command=self.delete_from_playlist,
            borderwidth=0,
            bg=bg_color3,
        )

        self.button_add.grid(row=1, column=0, padx=10)
        self.button_delete.grid(row=1, column=1, padx=10)

        play_image = Image.open(playUrl)
        play_image = play_image.resize((32, 32))
        self.play_photo = ImageTk.PhotoImage(play_image)

        stop_image = Image.open(stopUrl)
        stop_image = stop_image.resize((32, 32))
        self.stop_photo = ImageTk.PhotoImage(stop_image)

        next_image = Image.open(nextUrl)
        next_image = next_image.resize((32, 32))
        self.next_photo = ImageTk.PhotoImage(next_image)

        prev_image = Image.open(prevUrl)
        prev_image = prev_image.resize((32, 32))
        self.prev_photo = ImageTk.PhotoImage(prev_image)

        self.button_prev = tk.Button(
            control_frame, image=self.prev_photo, command=self.prev_track, borderwidth=0, bg=bg_color3
        )
        self.button_play = tk.Button(
            control_frame, image=self.play_photo, command=self.toggle_play, borderwidth=0, bg=bg_color3
        )
        self.button_next = tk.Button(
            control_frame, image=self.next_photo, command=self.next_track, borderwidth=0, bg=bg_color3
        )

        self.button_prev.grid(row=2, column=0, padx=10)
        self.button_play.grid(row=2, column=1, padx=10)
        self.button_next.grid(row=2, column=2, padx=10)

        self.volume_scale = ttk.Scale(
            control_frame,
            orient='horizontal',
            length=200,
            from_=0.0,
            to=1.0,
            command=self.set_volume,
            variable=tk.DoubleVar(value=1.0),
        )
        self.volume_scale.grid(row=3, column=0, columnspan=4, pady=10)

        pygame.mixer.init()

    def resize_image(self, path, size):
        image = Image.open(path)
        image = image.resize(size)
        return image

    def load_songs(self):
        self.playlist = filedialog.askopenfilenames(
            filetypes=[("Archivos MP3", "*.mp3")]
        )
        self.update_playlist_display()

    def update_playlist_display(self):
        self.playlist_display.delete(0, tk.END)
        for song in self.playlist:
            song_name = os.path.basename(song)
            self.playlist_display.insert(tk.END, song_name)

    def toggle_play(self):
        if not self.playlist:
            return
        if self.playing:
            self.stop_music()
        else:
            self.play_music()
    
    def toggle_delay(self):
        self.delay_enabled = not self.delay_enabled

    def play_music(self):
        if not self.playlist:
            return
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
        else:
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play(start=self.current_position)
            self.playing = True
            self.button_play.configure(image=self.stop_photo)
            current_song = os.path.basename(self.playlist[self.current_track])
            self.filename_label.config(text=current_song)
            self.current_position = self.current_position
    
    def play_music_with_delay(self):
        if not self.playlist:
            return
        delay_time = 500  # Ajusta este valor según tus necesidades
        delay(self.playlist[self.current_track], delay_time)
        pygame.mixer.music.load(self.playlist[self.current_track])
        pygame.mixer.music.play(start=self.current_position)
        self.playing = True
        self.button_play.configure(image=self.stop_photo)
        current_song = os.path.basename(self.playlist[self.current_track])
        self.filename_label.config(text=f"{current_song} - con Delay")
        self.current_position = self.current_position


    def stop_music(self):
        self.current_position = pygame.mixer.music.get_pos()
        pygame.mixer.music.stop()
        self.playing = False
        self.button_play.configure(image=self.play_photo)

    def add_to_playlist(self):
        song = filedialog.askopenfilename(filetypes=[("Archivos MP3", "*.mp3")])
        if song:
            self.playlist.append(song)
            self.update_playlist_display()

    def delete_from_playlist(self):
        selected_index = self.playlist_display.curselection()
        if selected_index:
            index = int(selected_index[0])
            del self.playlist[index]
            self.update_playlist_display()

    def next_track(self):
        if not self.playlist:
            return
        self.current_track = (self.current_track + 1) % len(self.playlist)
        if self.playing:
            self.play_music()

    def prev_track(self):
        if not self.playlist:
            return
        self.current_track = (self.current_track - 1) % len(self.playlist)
        if self.playing:
            self.play_music()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

def main():
    root = tk.Tk()
    reproductor = ReproductorMusica(root, lambda: toggle_theme(root))
    root.mainloop()

if __name__ == "__main__":
    main()
