# player.py

import pygame

def play_media():
    """Відтворення медіа"""
    pygame.mixer.init()
    pygame.mixer.music.load("media.mp3")
    pygame.mixer.music.play()

def stop_media():
    """Зупинка медіа"""
    pygame.mixer.music.stop()
