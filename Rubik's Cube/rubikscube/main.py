# Pygame is used to create the window that renders the cube
import pygame
from pygame.locals import *

# Tkinter is used to create the form that controls the cube
import tkinter as tk
from tkinter import *

# OpenGL is the graphics engine that renders the cube
from OpenGL.GL import *
from OpenGL.GLU import *

# RubixCube is the class that encapsulates a Rubix Cube
from rubikscube.RubiksCube import RubiksCube

# RenderCube is the module that handles the rendering of the cube
from rubikscube.RenderCube import render_rubiks_cube


# Defines the main module
def main():

    # Creates the Rubix Cube object which is displayed
    a = RubiksCube()

    # makemove generates a function which performs a move on the rubix cube
    def makemove(turn):
        def move():
            a.move(turn)

        return move

    # root is the form which acts as the controller for the rubix cube
    root = tk.Tk()
    root.wm_title('Command Window')

    # buttonwin is the window that contains all the move buttons
    buttonwin = tk.Frame(root, width=75, height=600)
    buttonwin.pack()

    # Contains all the elementary moves of the rubix cube
    moveset = ["R", "L", "U", "D", "F", "B", "M", "E", "S", "x", "y", "z"]

    # For every move M, add M, M2 and M' to the form
    for move in moveset:
        # Creates a button frame for the new buttons
        buttonframe = tk.Frame(buttonwin, width=75, height=50)
        buttonframe.pack()

        # Adds the buttons to the new frame
        tk.Button(buttonframe, text=move, command=makemove(move)).pack(side=LEFT)
        tk.Button(buttonframe, text=move + "2", command=makemove(move + "2")).pack(side=LEFT)
        tk.Button(buttonframe, text=move + "'", command=makemove(move + "'")).pack(side=LEFT)

    # Creates a frame for the rotation sliders
    sliderframe = tk.Frame(buttonwin, width=75, height=50)
    sliderframe.pack()

    # xrotate controls the horizontal rotation of the cube
    xrotate = Scale(sliderframe, from_=-180, to=180, bigincrement=90, sliderlength=20, label='rotate x-axis',
                    orient=HORIZONTAL)
    xrotate.pack(side=TOP)
    xrotate.set(0)

    # yrotate controls the vertical rotation of the cube
    yrotate = Scale(sliderframe, from_=-90, to=90, bigincrement=90, sliderlength=20, label="rotate y-axis",
                    orient=HORIZONTAL)
    yrotate.pack(side=TOP)
    yrotate.set(0)

    # The scramble button scrambles the cube
    tk.Button(buttonwin, text='Scramble', command=lambda: a.scramble()).pack()

    # The control window cannot be resized
    root.resizable(False, False)

    # Stops the command window from being deleted
    def donothing():
        pass

    root.protocol('WM_DELETE_WINDOW', donothing)

    # Loads control window
    root.update()

    # Creates OpenGL window in pygame to render the rubix cube
    display = (600, 600)
    pygame.init()
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption('Rubix Cube')

    # Loads the display
    pygame.display.flip()

    # Sets initial camera settings
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)
    glLineWidth(6)
    glEnable(GL_DEPTH_TEST)

    glPolygonOffset(-3.0, 3.0)

    # Sets initial orientation of the cube
    glRotatef(-90, 0, 1, 0)
    glRotatef(-90, 1, 0, 0)

    # x_curr and y_curr store the current rotation settings of the cube
    x_curr = 0
    y_curr = 0

    # Event loop
    while True:

        # If quit is clicked, exit the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                root.destroy()
                quit()

        # Gets current rotation settings
        x_rotate_val = xrotate.get()
        y_rotate_val = yrotate.get()

        # Undoes previous and sets current rotation
        glRotatef(-y_curr, 0, 1, 0)
        glRotatef(-x_curr, 0, 0, 1)
        glRotatef(x_rotate_val, 0, 0, 1)
        glRotatef(y_rotate_val, 0, 1, 0)

        # Stores new rotation settings
        x_curr, y_curr = x_rotate_val, y_rotate_val

        # Clears color buffer and depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Renders the Rubix Cube
        render_rubiks_cube(a)

        # Updates pygame and tkinter form
        pygame.display.flip()
        root.update()


# If file is run directly execute the main() method
if __name__ == '__main__':
    main()
