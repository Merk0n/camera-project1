import numpy as np
import pygame
from pygame.locals import *

# Inicjalizacja Pygame i ustawienie parametrów okna gry
pygame.init()
width, height = 800, 600  # Wymiary okna
screen = pygame.display.set_mode((width, height))  # Inicjalizacja ekranu gry
clock = pygame.time.Clock()  # Zegar do kontroli szybkości aktualizacji ekranu

# Funkcje do tworzenia macierzy transformacji
def translation_matrix(dx, dy, dz):
    # Tworzy macierz translacji o wektor (dx, dy, dz)
    return np.array([
        [1, 0, 0, dx],
        [0, 1, 0, dy],
        [0, 0, 1, dz],
        [0, 0, 0, 1]
    ])

def rotation_matrix_y(angle):
    # Tworzy macierz rotacji wokół osi Y o kąt 'angle' (w radianach)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [cos_a, 0, sin_a, 0],
        [0,     1, 0,     0],
        [-sin_a, 0, cos_a, 0],
        [0,     0, 0,     1]
    ])

def rotation_matrix_x(angle):
    # Tworzy macierz rotacji wokół osi X o kąt 'angle' (w radianach)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [1, 0,     0,      0],
        [0, cos_a, -sin_a, 0],
        [0, sin_a, cos_a,  0],
        [0, 0,     0,      1]
    ])

def rotation_matrix_z(angle):
    # Tworzy macierz rotacji wokół osi Z o kąt 'angle' (w radianach)
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    return np.array([
        [cos_a, -sin_a, 0, 0],
        [sin_a, cos_a,  0, 0],
        [0,     0,      1, 0],
        [0,     0,      0, 1]
    ])

def update_view_matrix():
    # Aktualizuje macierz widoku na podstawie obecnej orientacji i pozycji kamery
    pitch_matrix = rotation_matrix_x(camera_pitch)
    yaw_matrix = rotation_matrix_y(camera_angle)
    roll_matrix = rotation_matrix_z(camera_roll)
    return np.linalg.inv(roll_matrix @ pitch_matrix @ yaw_matrix @ translation_matrix(*camera_pos))

def perspective_matrix(fov, aspect, near, far):
    # Tworzy macierz projekcji perspektywicznej na podstawie podanych parametrów
    f = 1 / np.tan(fov / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ])

def draw_line(screen, v1, v2, width, height):
    # Rysuje linię na ekranie między dwoma punktami 3D po ich projekcji na 2D
    x1, y1, z1, w1 = v1 / v1[3]
    x2, y2, z2, w2 = v2 / v2[3]
    x1, y1 = int((x1 + 1) * 0.5 * width), int((1 - y1) * 0.5 * height)
    x2, y2 = int((x2 + 1) * 0.5 * width), int((1 - y2) * 0.5 * height)
    pygame.draw.line(screen, (255, 255, 255), (x1, y1), (x2, y2))

def draw_cube(screen, cube_vertices, cube_edges, mvp_matrix, width, height):
    # Rysuje sześcian na podstawie wierzchołków i krawędzi
    for edge in cube_edges:
        v1 = mvp_matrix @ cube_vertices[edge[0]]
        v2 = mvp_matrix @ cube_vertices[edge[1]]
        draw_line(screen, v1, v2, width, height)

# Definicja wierzchołków i krawędzi sześcianu
cube_vertices = np.array([[x, y, z, 1] for x in [-1, 1] for y in [-1, 1] for z in [-1, 1]])
cube_edges = [(0, 1), (1, 3), (3, 2), (2, 0), (0, 4), (1, 5), (3, 7), (2, 6), (4, 5), (5, 7), (7, 6), (6, 4)]

# Inicjalizacja zmiennych kamery
camera_pos = np.array([0.0, 0.0, -20.0])  # Pozycja kamery
camera_angle = 0  # Kąt obrotu wokół osi Y (yaw)
camera_pitch = 0  # Kąt obrotu wokół osi X (pitch)
camera_roll = 0   # Kąt obrotu wokół osi Z (roll)
camera_fov = np.pi / 4  # Kąt widzenia kamery (field of view)
camera_speed = 0.5  # Prędkość przemieszczania się kamery
rotation_speed = 0.05  # Prędkość obrotu kamery

# Główna pętla gry
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            # Sterowanie kamerą
            if event.key == pygame.K_s:  # Przód
                camera_pos -= camera_speed * np.array([np.sin(camera_angle), 0, np.cos(camera_angle)])
            if event.key == pygame.K_w:  # Tył
                camera_pos += camera_speed * np.array([np.sin(camera_angle), 0, np.cos(camera_angle)])
            if event.key == pygame.K_d:  # Obrót w lewo
                camera_angle += rotation_speed
            if event.key == pygame.K_a:  # Obrót w prawo
                camera_angle -= rotation_speed

            # Dodatkowe sterowanie
            if event.key == pygame.K_q:  # Obrót kamery w lewo
                camera_roll += rotation_speed
            if event.key == pygame.K_e:  # Obrót kamery w prawo
                camera_roll -= rotation_speed
            if event.key == pygame.K_r:  # Zoom in (przybliżenie)
                camera_fov -= 0.01
            if event.key == pygame.K_t:  # Zoom out (oddalenie)
                camera_fov += 0.01
            if event.key == pygame.K_x:  # Pochylenie kamery w górę
                camera_pitch += rotation_speed
            if event.key == pygame.K_z:  # Pochylenie kamery w dół
                camera_pitch -= rotation_speed

    screen.fill((0, 0, 0))  # Czyszczenie ekranu

    # Ustawienie macierzy projekcji i widoku
    projection = perspective_matrix(camera_fov, width / height, 0.1, 1000)
    view_matrix = update_view_matrix()
    
    # Rysowanie sześcianów
    for z in [-5, -10]:  # Dwa sześciany z przodu, dwa za nimi
        for x in [-5, 5]:  # Sześciany rozmieszczone po lewej i prawej stronie
            model_matrix = translation_matrix(x, 0, z)  # Przesunięcie w osiach X i Z
            mvp_matrix = projection @ view_matrix @ model_matrix
            draw_cube(screen, cube_vertices, cube_edges, mvp_matrix, width, height)

    pygame.display.flip()  # Aktualizacja zawartości okna
    clock.tick(60)  # Utrzymanie stałej liczby klatek na sekundę

pygame.quit()  # Zakończenie pracy Pygame
