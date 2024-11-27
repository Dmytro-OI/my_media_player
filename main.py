import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import threading
import webbrowser
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
import winreg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import webbrowser

# --- Глобальні змінні ---
APP_FOLDER = os.path.expanduser("~\\my_media_player")
playlist = []  
current_track_index = 0
logo_x, logo_y, logo_direction = 10, 10, 1
paused = False
volume = 0.5  
CORRECT_PASSWORD = "505"

# Створюємо спеціалізований каталог
if not os.path.exists(APP_FOLDER):
    os.makedirs(APP_FOLDER)

# --- Функція перевірки пароля ---
def check_password(root):
    """Запит пароля при запуску програми"""
    password = simpledialog.askstring("Password", "Enter password to continue:", show='*', parent=root)
    
    if password == CORRECT_PASSWORD:
        print("Password is correct. Running the program.")
        root.deiconify()  
        create_ui(root)  
    else:
        print("Incorrect password. Exiting.")
        messagebox.showerror("Error", "Incorrect password. The program will now exit.")
        root.destroy()  

def search_track():
    """Шукає поточний трек в Google."""
    if playlist:
        track_name = os.path.basename(playlist[current_track_index])  
        search_url = f"https://www.google.com/search?q={track_name}"  
        webbrowser.open(search_url)
        print(f"Searching track: {search_url}")
    else:
        messagebox.showerror("Error", "Playlist is empty!")  
        
# --- Функції для роботи з реєстром ---
def save_settings_to_registry():
    try:
        reg_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\MyMediaPlayer")
        winreg.SetValueEx(reg_key, "playlist", 0, winreg.REG_SZ, ";".join(playlist))
        winreg.SetValueEx(reg_key, "current_track_index", 0, winreg.REG_DWORD, current_track_index)
        winreg.CloseKey(reg_key)
    except Exception as e:
        print(f"Error saving to registry: {e}")

def load_settings_from_registry():
    global playlist, current_track_index
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\MyMediaPlayer", 0, winreg.KEY_READ)
        playlist = winreg.QueryValueEx(reg_key, "playlist")[0].split(";")
        current_track_index = winreg.QueryValueEx(reg_key, "current_track_index")[0]
        winreg.CloseKey(reg_key)
    except Exception:
        playlist = []
        current_track_index = 0

# --- Функції для роботи з медіа ---
def add_to_playlist():
    files = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if files:
        playlist.extend(files)
        save_settings_to_registry()
        update_playlist_display()
        print(f"Added to playlist: {files}")

def play_media():
    global paused, current_track_index
    if playlist:
        pygame.mixer.init()
        if paused:
            pygame.mixer.music.unpause()
            paused = False
            print("Media resumed")
        else:
            pygame.mixer.music.load(playlist[current_track_index])
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play()
            print(f"Playing media: {playlist[current_track_index]}")
            update_song_display()
    else:
        messagebox.showerror("Error", "Playlist is empty!")

def pause_media():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        paused = True
        print("Media paused")

def stop_media():
    global paused
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        paused = False
        print("Media stopped")

def next_track():
    global current_track_index
    if playlist:
        current_track_index = (current_track_index + 1) % len(playlist)
        save_settings_to_registry()
        play_media()
    else:
        messagebox.showerror("Error", "Playlist is empty!")

def previous_track():
    global current_track_index
    if playlist:
        current_track_index = (current_track_index - 1) % len(playlist)
        save_settings_to_registry()
        play_media()
    else:
        messagebox.showerror("Error", "Playlist is empty!")

def set_volume(value):
    global volume
    volume = float(value) / 100
    pygame.mixer.music.set_volume(volume)
    print(f"Volume set to {volume * 100}%")

def update_song_display():
    song_label.config(text=f"Now Playing: {os.path.basename(playlist[current_track_index])}")

def update_playlist_display():
    playlist_box.delete(0, tk.END)  
    for track in playlist:
        playlist_box.insert(tk.END, os.path.basename(track))  


# --- Функції для логотипу ---
def create_moving_logo_in_playlist(playlist_box):
    """Створюємо логотип, який рухається всередині списку треків."""
    global logo_x, logo_y

    label = tk.Label(playlist_box, text="Гринчишин Д. ОІ-22", font=("Arial", 12, "bold"), bg="blue", fg="white")
    label.place(x=logo_x, y=logo_y)
    move_logo_in_playlist(playlist_box, label)

def move_logo_in_playlist(playlist_box, label):
    """Рух логотипа в межах списку треків."""
    global logo_x, logo_y, logo_direction

    max_x = playlist_box.winfo_width() - label.winfo_width()
    max_y = playlist_box.winfo_height() - label.winfo_height()

    if logo_x <= 0 or logo_x >= max_x:
        logo_direction *= -1
    logo_x += logo_direction * 5
    logo_y += logo_direction * 3
    label.place(x=logo_x, y=logo_y)
    playlist_box.after(50, move_logo_in_playlist, playlist_box, label)

# --- Функції для 3D графіки ---
def open_3d_window():
    """Відкриває 3D вікно з використанням Voxels у Matplotlib."""
    
    # Створення осей
    axes = [5, 5, 5]
    
    # Створення даних для графіка
    data = np.ones(axes, dtype=np.bool)

    # Налаштування прозорості
    alpha = 0.9
    
    # Налаштування кольору
    colors = np.empty(axes + [4], dtype=np.float32)
    colors[:] = [1, 0, 0, alpha]  # червоний з прозорістю
    
    # Створення графіка
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    # Використання Voxels для налаштування розмірів, позицій і кольорів
    ax.voxels(data, facecolors=colors)

    # Показ графіка
    plt.show()

# --- Функції для Інтернету ---
def search_track():
    if playlist:
        track_name = os.path.basename(playlist[current_track_index])
        search_url = f"https://www.google.com/search?q={track_name}"
        webbrowser.open(search_url)
        print(f"Searching track: {search_url}")
    else:
        messagebox.showerror("Error", "Playlist is empty!")

# --- Клік мишкою ---
def log_mouse_click(event):
    print(f"Mouse clicked at: ({event.x}, {event.y})")

# --- Управління клавіатурою ---
def bind_keyboard_shortcuts(root):
    root.bind("<space>", lambda e: play_media())
    root.bind("<s>", lambda e: stop_media())
    root.bind("<p>", lambda e: pause_media())
    root.bind("<Right>", lambda e: next_track())
    root.bind("<Left>", lambda e: previous_track())
    
def delete_track():
    """Видаляє вибраний трек зі списку відтворення."""
    global current_track_index

    selected_index = playlist_box.curselection()  
    print(f"Selected index: {selected_index}")  
    print(f"Current playlist: {playlist}")  

    if selected_index:
        selected_index = selected_index[0]  
        if 0 <= selected_index < len(playlist):  
            deleted_track = playlist.pop(selected_index)  
            print(f"Deleted track: {deleted_track}")

            if selected_index == current_track_index and pygame.mixer.music.get_busy():
                stop_media()

            if current_track_index > selected_index:
                current_track_index -= 1  
            elif current_track_index == len(playlist): 
                current_track_index = max(0, len(playlist) - 1)

            if not playlist:
                current_track_index = 0
                song_label.config(text="No song playing")

            update_playlist_display()
            save_settings_to_registry()

        else:
            print(f"Error: Selected index {selected_index} is out of playlist bounds.")
    else:
        messagebox.showerror("Error", "No track selected for deletion!")


# --- Створення UI ---
def create_ui(root):
    global song_label, playlist_box
    root.title("Мультимедійний плеєр")
    root.geometry("770x400")

    song_label = tk.Label(root, text="No song playing", bg="gray", fg="black", font=("Arial", 12), height=2)
    song_label.pack(fill=tk.X)

    playlist_box = tk.Listbox(root, height=10)
    playlist_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    playlist_box.bind("<Button-1>", log_mouse_click)

    control_frame = tk.Frame(root)
    control_frame.pack()

    tk.Button(control_frame, text="Add to Playlist", command=add_to_playlist).grid(row=0, column=0, padx=5)
    tk.Button(control_frame, text="Play", command=play_media).grid(row=0, column=1, padx=5)
    tk.Button(control_frame, text="Pause", command=pause_media).grid(row=0, column=2, padx=5)
    tk.Button(control_frame, text="Stop", command=stop_media).grid(row=0, column=3, padx=5)
    tk.Button(control_frame, text="Next", command=next_track).grid(row=0, column=4, padx=5)
    tk.Button(control_frame, text="Previous", command=previous_track).grid(row=0, column=5, padx=5)
    tk.Button(control_frame, text="Delete Track", command=delete_track).grid(row=0, column=6, padx=5)
    tk.Button(control_frame, text="Search Track in Google", command=search_track).grid(row=0, column=7, padx=5)
    tk.Button(control_frame, text="3D Object", command=open_3d_window).grid(row=0, column=8, padx=5)


    volume_slider = tk.Scale(control_frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", command=set_volume)
    volume_slider.set(50) 
    volume_slider.grid(row=0, column=9, padx=5)

    load_settings_from_registry()
    update_playlist_display()
    create_moving_logo_in_playlist(playlist_box)
    bind_keyboard_shortcuts(root)

    # Гарячі клавіші
    root.bind("<Delete>", lambda e: delete_track())  
    root.bind("<s>", lambda e: stop_media()) 
    root.bind("<p>", lambda e: pause_media())  
    root.bind("<space>", lambda e: play_media())  
    root.bind("<Right>", lambda e: next_track())  
    root.bind("<Left>", lambda e: previous_track())  
    root.bind("<g>", lambda e: search_track())  

# --- Видалення треку кнопкою Delete ---
def bind_keyboard_shortcuts(root):
    root.bind("<space>", lambda e: play_media())
    root.bind("<s>", lambda e: stop_media())
    root.bind("<p>", lambda e: pause_media())
    root.bind("<Right>", lambda e: next_track())
    root.bind("<Left>", lambda e: previous_track())
    root.bind("<Delete>", lambda e: delete_track())  

# --- Основний запуск програми ---
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    check_password(root)
    root.mainloop()
