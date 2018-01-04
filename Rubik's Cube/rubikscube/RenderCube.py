# OpenGL is the graphics engine that renders the cube
from OpenGL.GL import *

# RubiksCube is the class that encapsulates a Rubik's Cube
from rubikscube.RubiksCube import RubiksCube


# Returns the vertices of a 1x1 square in the xy plane with top corner at (x, y, z)
def xy_tile(x, y, z):
    return (
        (x, y, z),
        (x + 1, y, z),
        (x + 1, y + 1, z),
        (x, y + 1, z)
    )


# Returns the vertices of a 1x1 square in the xz plane with top corner at (x, y, z)
def xz_tile(x, y, z):
    return (
        (x, y, z),
        (x + 1, y, z),
        (x + 1, y, z + 1),
        (x, y, z + 1)
    )


# Returns the vertices of a 1x1 square in the yz plane with top corner at (x, y, z)
def yz_tile(x, y, z):
    return (
        (x, y, z),
        (x, y + 1, z),
        (x, y + 1, z + 1),
        (x, y, z + 1)
    )


# Returns a list of faces on a 3x3 grid in the xy plane centered on x = 0, y = o
def xy_face(z):
    return [[xy_tile(x - 1.5, y - 1.5, z) for x in range(3)] for y in range(3)]


# Returns a list of faces on a 3x3 grid in the xz plane centered on x = 0, z = o
def xz_face(y):
    return [[xz_tile(x - 1.5, y, z - 1.5) for x in range(3)] for z in range(3)]


# Returns a list of faces on a 3x3 grid in the yz plane centered on y = 0, z = o
def yz_face(x):
    return [[yz_tile(x, y - 1.5, z - 1.5) for y in range(3)] for z in range(3)]


# Renders a Rubik's Cube
def render_rubiks_cube(cube: RubiksCube):
    # Defines the colors that correspond to the tile values
    cube_colors = {
        'W': (1, 1, 1),
        'R': (1, 0, 0),
        'B': (0, 0, 1),
        'Y': (1, 1, 0),
        'O': (1, 0.5, 0),
        'G': (0, 1, 0)
    }

    # Defines edge index pairings
    edge_index = ((0, 1), (1, 2), (2, 3), (3, 0))

    # Defines face index set
    face_index = (0, 1, 2, 3)

    # Renders faces
    glBegin(GL_QUADS)

    # Renders colors of top face
    top = xy_face(1.5)
    for x in range(3):
        for y in range(3):
            for vertex in face_index:
                glColor3fv(cube_colors[cube.top[y][x]])
                glVertex3fv(top[x][y][vertex])

    # Renders colors of bottom face
    bot = xy_face(-1.5)
    for x in range(3):
        for y in range(3):
            for vertex in face_index:
                glColor3fv(cube_colors[cube.bot[2 - y][x]])
                glVertex3fv(bot[x][y][vertex])

    # Renders colors of left face
    left = xz_face(-1.5)
    for x in range(3):
        for y in range(3):
            for vertex in face_index:
                glColor3fv(cube_colors[cube.left[2 - x][y]])
                glVertex3fv(left[x][y][vertex])

    # Renders colors of right face
    right = xz_face(1.5)
    for x in range(3):
        for y in range(3):
            for vertex in face_index:
                glColor3fv(cube_colors[cube.right[2 - x][2 - y]])
                glVertex3fv(right[x][y][vertex])

    # Renders colors on back face
    back = yz_face(-1.5)
    for x in range(3):
        for y in range(3):
            for vertex in face_index:
                glColor3fv(cube_colors[cube.back[2 - x][2 - y]])
                glVertex3fv(back[x][y][vertex])

    # Renders colors on front face
    front = yz_face(1.5)
    for x in range(3):
        for y in range(3):
            for vertex in face_index:
                glColor3fv(cube_colors[cube.front[2 - x][y]])
                glVertex3fv(front[x][y][vertex])

    # Stops rendering colors
    glEnd()

    # Renders lines
    glBegin(GL_LINES)

    # Sets color to black
    glColor3f(0, 0, 0)

    # Defines all the faces to be filled
    faces = (top, bot, front, back, left, right)

    # For every face of the cube, draw a 3x3 square grid
    for face in faces:
        for x in range(3):
            for y in range(3):
                for edge in edge_index:
                    for vertex in edge:
                        glVertex3fv(tuple(1.01 * x for x in face[x][y][vertex]))

    # Stops rendering lines
    glEnd()

