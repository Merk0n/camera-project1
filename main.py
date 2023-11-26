import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from draw import draw_scene
import math

# Inicjalizacja początkowej pozycji kamery oraz orientacji (pitch, yaw, roll) i zoomu.
camera_pos = [-10, 0, -1]
camera_pitch = 0
camera_yaw = 0
camera_roll = 0
zoom = 45

# Definicja funkcji obsługującej ruch i rotację kamery.
def movement(move_speed, rotation_speed):
    
    # Użycie zmiennych globalnych do przechowywania stanu kamery.
    global camera_pos, camera_yaw, camera_pitch, camera_roll, zoom
    
    # Pobranie stanu klawiatury.
    keys = pygame.key.get_pressed()

    # Obliczenie wektorów ruchu na podstawie orientacji kamery - ruch zgodny z kierunkiem kamery.
    yaw_rad = math.radians(camera_yaw)
    forward_vector = [math.sin(yaw_rad), 0, -math.cos(yaw_rad)]
    right_vector = [math.cos(yaw_rad), 0, math.sin(yaw_rad)]
    
    # Przesuwanie kamery w przód, tył i w boki za pomocą klawiszy 'a', 'd', 's' i 'w'.
    if keys[pygame.K_a]:
        camera_pos = [camera_pos[j] + move_speed * forward_vector[j] for j in range(3)]
    if keys[pygame.K_d]:
        camera_pos = [camera_pos[j] - move_speed * forward_vector[j] for j in range(3)]
    if keys[pygame.K_s]:
        camera_pos = [camera_pos[j] - move_speed * right_vector[j] for j in range(3)]
    if keys[pygame.K_w]:
        camera_pos = [camera_pos[j] + move_speed * right_vector[j] for j in range(3)]

    # Przechylenie kamery w lewo i prawo za pomocą klawiszy 'q' i 'e'
    if keys[pygame.K_e]:
        camera_roll -= rotation_speed
    if keys[pygame.K_q]:
        camera_roll += rotation_speed

    # Zmiana orientacji kamery za pomocą klawiszy strzałek.
    if keys[pygame.K_LEFT]:
        camera_yaw -= 1
    if keys[pygame.K_RIGHT]:
        camera_yaw += 1
    if keys[pygame.K_UP]:
        camera_pitch += 1
    if keys[pygame.K_DOWN]:
        camera_pitch -= 1
    # Ograniczenie kąta przechylenia kamery.
    camera_pitch = max(-89, min(89, camera_pitch)) 

    # Zoom
    if keys[pygame.K_r]:
        zoom -= 1
    if keys[pygame.K_t]:
        zoom += 1
    zoom = max(10, min(100, zoom))

    # Przesuwanie kamery w górę i dół za pomocą klawiszy 'z' i 'x'
    if keys[pygame.K_z]:
        camera_pos[1] += move_speed
    if keys[pygame.K_x]:
        camera_pos[1] -= move_speed

# Definicja funkcji do aktualizacji orientacji kamery.
def update_camera_direction():
    
    # Użycie zmiennych globalnych do przechowywania orientacji kamery.
    global camera_yaw, camera_pitch, camera_roll

    # Przekształcenie kątów orientacji kamery na radiany.
    yaw_rad = math.radians(camera_yaw)
    pitch_rad = math.radians(camera_pitch)

    # Obliczenie kierunku patrzenia kamery na podstawie jej orientacji.
    x = math.cos(pitch_rad) * math.cos(yaw_rad)
    y = math.sin(pitch_rad)
    z = math.cos(pitch_rad) * math.sin(yaw_rad)

    # Zastosowanie obracania (roll) kamery wokół osi Z.
    glRotatef(camera_roll, 0, 0, 1)

    # Ustawienie kamery w określonej pozycji, kierunku patrzenia i orientacji w przestrzeni.
    gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2],
              camera_pos[0] + x, camera_pos[1] + y, camera_pos[2] + z,
              0, 1, 0)


def main():
    # Inicjalizacja biblioteki Pygame.
    pygame.init()

    # Ustawienie wielkości okna gry.
    display = (1024, 768)

    # Włączenie podwójnego buforowania oraz wsparcia dla OpenGL.
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Ustawienie perspektywy kamery (kąt widzenia, proporcje szerokości do wysokości, zakres widzenia).
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    # Ustawienie prędkości ruchu i rotacji kamery.
    move_speed = 0.1
    rotation_speed = 2 

    # Główna pętla programu.
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Czyszczenie buforów koloru i głębi
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Resetowanie macierzy widoku
        glLoadIdentity()

        # Ustawienie perspektywy z uwzględnieniem zoomu
        gluPerspective(zoom, (display[0] / display[1]), 0.1, 50.0)
        
        # Wywołanie funkcji odpowiedzialnej za ruch kamery
        movement(move_speed, rotation_speed)

        # Aktualizacja kierunku, w którym skierowana jest kamera
        update_camera_direction()

        # Rysowanie sceny z "budynkami"
        draw_scene()

        # Aktualizacja wyświetlanego obrazu w oknie
        pygame.display.flip()

        # Krótka przerwa, aby ograniczyć szybkość wykonywania pętli
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
