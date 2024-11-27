import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame

logo_direction = 1
logo_x = 100
logo_y = 100

def create_moving_logo(root):
    """Створення рухомого логотипу"""
    label = tk.Label(root, text="bbno$", font=("Arial", 20, "bold"), fg="red", bg="black")
    label.place(x=logo_x, y=logo_y)
    move_logo(label)

def move_logo(label):
    """Рух логотипу"""
    global logo_x, logo_y, logo_direction
    if logo_x >= root.winfo_width() - 100 or logo_x <= 0:
        logo_direction *= -1
    logo_x += logo_direction * 5
    logo_y += logo_direction * 3
    label.place(x=logo_x, y=logo_y)
    root.after(50, move_logo, label)

def open_3d_window():
    """Відкриття 3D вікна"""
    def init_3d():
        glTranslatef(0.0, 0.0, -5)
        glRotatef(25, 3, 1, 1)

    def draw_cube():
        vertices = [
            (1, -1, -1),  (1, 1, -1),  (-1, 1, -1),  (-1, -1, -1),
            (1, -1, 1),   (1, 1, 1),    (-1, -1, 1),   (-1, 1, 1),
        ]
        surfaces = [
            (0, 1, 2, 3),  (3, 2, 7, 6),  (6, 7, 5, 4),  (4, 5, 1, 0),
            (1, 5, 7, 2),  (4, 0, 3, 6),
        ]
        glBegin(GL_QUADS)
        for surface in surfaces:
            for vertex in surface:
                glVertex3fv(vertices[vertex])
        glEnd()

    def main_3d():
        pygame.display.set_mode((640, 480), pygame.DOUBLEBUF | pygame.OPENGL)
        init_3d()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            draw_cube()
            pygame.display.flip()
            pygame.time.wait(10)

    pygame.init()
    pygame.display.set_mode((640, 480), pygame.DOUBLEBUF | pygame.OPENGL)
    main_3d()
