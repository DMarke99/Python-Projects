# Rubik's Cube Project

A fully functional Rubik's Cube coded in Python, equipped with all the standard Rubik's Cube moves

## Prerequisites

To open and run the project on your computer you will need

```
Tkinter 8.5+ (Version 8.5.0 is used in the project)
Python 3.6+
Pygame 1.9.3+
PyOpenGL 3.1.0+
```

## Setup

1) Ensure you have the above dependencies installed.
2) Download the [Rubix Cube Project Folder](https://github.com/DMarke99/Python-Projects/tree/master/Rubik's%20Cube).
3) Execute by running [rubikscube/main.py](https://github.com/DMarke99/Python-Projects/blob/master/Rubik's%20Cube/rubikscube/main.py)

## Usage

#### Commands
```
~ Standard moves ~
R: Rotate the right layer of the cube 90 degrees clockwise.
L: Rotate the left layer of the cube 90 degrees clockwise.
U: Rotate the top layer of the cube 90 degrees clockwise.
D: Rotate the bottom layer of the cube 90 degrees clockwise.
F: Rotate the front layer of the cube 90 degrees clockwise.
B: Rotate the back layer of the cube 90 degrees clockwise.
M: Rotate the middle layer of the cube 90 degrees in the same direction as L.
E: Rotate the equatorial layer of the cube 90 degrees in the same direction as D.
S: Rotate the right layer of the cube 90 degrees in the same direction as F.
x: Rotate the whole cube 90 degrees in the same direction as R.
y: Rotate the whole cube 90 degrees in the same direction as U.
z: Rotate the whole cube 90 degrees in the same direction as F.

~ Move augmentations ~
M': Perform the opposite of move M. This always equates to performing move M 3 times.
M2: Perform move M twice.

~ View controls ~
x rotate: rotates the cube horizontally. Ranges from -180 to 180 degrees.
y rotate: rotates the cube vertically. Ranges from -90 to 90 degrees.

~ Other controls ~
Scramble: scrambles the cube by performing 100 randomly selected moves.

*moves are with respect to the red face being the front face and the white face being the top face. This is changed when performing moves x, y and z.
```

#### Basic Usage
The Rubix Cube will be displayed on the pygame window

The controls are displayed on the tkinter window

Click any of the control buttons to perform a move on the Rubik's Cube

Slide the slider to change the orientation of the cube

## Contributers

This project was created entirely by myself over 2-3 days in my Michaelmas break. The greatest challenge was learning how to use OpenGL to render the cube, and learning how tkinter and pygame worked.
