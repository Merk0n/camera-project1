import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from camera import *
from draw import *

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
