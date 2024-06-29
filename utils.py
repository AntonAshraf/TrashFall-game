from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import pygame
from settings import *


def render_iamge_background(image_path):
    # load the background image and make it fit the window size
    background = pygame.image.load(image_path)
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
    background_data = pygame.image.tostring(background, "RGB", True)
    glRasterPos2d(0, 0)
    glDrawPixels(WINDOW_WIDTH, WINDOW_HEIGHT, GL_RGB, GL_UNSIGNED_BYTE, background_data)


def sliding_text():
    global sliding_text_offset
    # Display sliding text
    glColor3f(1, 0, 1)
    glRasterPos2i(int(sliding_text_offset), WINDOW_HEIGHT - 30)  # Convert to integer
    sliding_text = "Welcome to Trash Fall Game"
    for char in sliding_text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
        sliding_text_offset += 0.1  # Adjust the sliding speed as needed (much slower movement)
        # Reset the sliding offset if it goes beyond the window width
        if sliding_text_offset > WINDOW_WIDTH:
            sliding_text_offset = -120  # Reset the offset to the starting position  
