from OpenGL.GL import *

# Definicja funkcji do rysowania sześcianu.
def draw_cube():

    # Rozpoczęcie rysowania linii.
    glBegin(GL_LINES)

    # Definicja wierzchołków sześcianu.
    vertices = [
        [1, -1, -1], [1, 1, -1], [-1, 1, -1], [-1, -1, -1],  # Back face
        [1, -1, 1], [1, 1, 1], [-1, -1, 1], [-1, 1, 1],      # Front face
        [1, -1, -1], [1, 1, -1], [1, 1, 1], [1, -1, 1],      # Right face
        [-1, -1, 1], [-1, 1, 1], [-1, 1, -1], [-1, -1, -1],  # Left face
        [-1, 1, -1], [1, 1, -1], [1, 1, 1], [-1, 1, 1],      # Top face
        [-1, -1, 1], [1, -1, 1], [1, -1, -1], [-1, -1, -1]   # Bottom face
    ]

    # Definicja krawędzi sześcianu.
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # Tylna ściana
        (4, 5), (5, 7), (7, 6), (6, 4),  # Przednia ściana
        (0, 4), (1, 5), (2, 7), (3, 6),  # Połączenia ścian bocznych
        (0, 4), (1, 5), (2, 7), (3, 6),  # Połączenia ścian górnych i dolnych
        (8, 9), (9, 10), (10, 11), (11, 8),  # Prawa ściana
        (12, 13), (13, 14), (14, 15), (15, 12),  # Lewa ściana
        (16, 17), (17, 18), (18, 19), (19, 16),  # Górna ściana
        (20, 21), (21, 22), (22, 23), (23, 20)   # Dolna ściana
    ]

    # Rysowanie każdej krawędzi sześcianu.
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Definicja funkcji do rysowania sceny.
def draw_scene():

    # Rysowanie wielu sześcianów w scenie w różnych pozycjach.
    for x in range(-5, 6, 4):
        for z in range(-5, 6, 4):
            glPushMatrix()
            glTranslatef(x, 0, z)
            draw_cube()
            glPopMatrix()
