import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import pygame
from settings import bin_x, trash_x, trash_y, score, lives, game_over, game_running, WINDOW_WIDTH, WINDOW_HEIGHT, BIN_SIZE, TRASH_SIZE, TRASH_SPEED, background_music, game_over_sound, trash_sound, trash2_sound, trash3_sound, collect, yay
from game_objects import draw_clouds, draw_flowers, draw_trees, draw_sky, draw_skyline, draw_grass, draw_wooden_bench, draw_circle
from utils import render_iamge_background, sliding_text
import random


def draw_background():
    draw_sky()
    draw_skyline()
    draw_grass()
    draw_flowers()
    draw_trees()
    draw_wooden_bench(100, 150, 150, 20, 50, (0.4, 0.2, 0.0), (0.3, 0.15, 0.0))  # First bench
    draw_wooden_bench(500, 150, 150, 20, 50, (0.4, 0.2, 0.0), (0.3, 0.15, 0.0))  # Second bench

def update(value):
    global trash_y, trash_x, score, lives, game_running, game_over

    if game_running and not game_over:
        trash_y -= TRASH_SPEED
        game_over_sound.stop()
        # Check if trash caught by bin
        if trash_y < 100 and bin_x - BIN_SIZE // 2 < trash_x + TRASH_SIZE // 2 < bin_x + BIN_SIZE // 2:
            score += 1
            trash_y = WINDOW_HEIGHT
            trash_x = random.randint(0, WINDOW_WIDTH)
            collect.play()  
            if score % 10 == 0:
                lives += 1
                yay.play()
        # Check if trash missed
        if trash_y < 0:
            trash_y = WINDOW_HEIGHT
            trash_x = random.randint(0, WINDOW_WIDTH)
            lives -= 1 
            # randomize the trash sound
            random_sound = random.randint(1, 3)
            if random_sound == 1:
                trash_sound.play()
            elif random_sound == 2:
                trash2_sound.play()
            else:
                trash3_sound.play()
            
            if lives == 0:
                game_over = True  
                game_over_sound.play()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global bin_x, game_running, game_over, lives, score

    if game_over:
        if key == b'r':  # Retry
            lives = 3
            score = 0
            game_over = False
            game_running = True
        elif key == b'q':  # Quit
            # Exit pygame
            pygame.quit()
            # Exit OpenGL
            glutLeaveMainLoop()

    elif not game_running:
        if key == b' ':  # Start game on space key press
            game_running = True
            background_music.play(-1)

    else:  # Game running
        if key == b'\x1b':
            sys.exit(0)
        elif key == b'a' and bin_x > BIN_SIZE // 2:
            bin_x -= 20
        elif key == b'd' and bin_x < WINDOW_WIDTH - BIN_SIZE // 2:
            bin_x += 20
            
def draw_trash():
    # Main body of the trash
    glColor3f(0.5, 0.3, 0.0)  # Set trash color to brown
    glBegin(GL_QUADS)
    glVertex2f(trash_x, trash_y)
    glVertex2f(trash_x + TRASH_SIZE, trash_y)
    glVertex2f(trash_x + TRASH_SIZE, trash_y + TRASH_SIZE)
    glVertex2f(trash_x, trash_y + TRASH_SIZE)
    glEnd()

    # Detail: Trash stripes
    stripe_width = TRASH_SIZE / 10
    glColor3f(0.3, 0.2, 0.0)  # Darker shade for stripes
    for i in range(1, 5):
        glBegin(GL_QUADS)
        glVertex2f(trash_x + i * stripe_width * 2, trash_y)
        glVertex2f(trash_x + i * stripe_width * 2 + stripe_width, trash_y)
        glVertex2f(trash_x + i * stripe_width * 2 + stripe_width, trash_y + TRASH_SIZE)
        glVertex2f(trash_x + i * stripe_width * 2, trash_y + TRASH_SIZE)
        glEnd()

    # Detail: Crumpled effect
    glColor3f(0.4, 0.25, 0.0)  # Slightly different brown for texture
    glBegin(GL_POINTS)
    for i in range(100):  # Add 100 points for crumpled effect
        point_x = trash_x + random.uniform(0, TRASH_SIZE)
        point_y = trash_y + random.uniform(0, TRASH_SIZE)
        glVertex2f(point_x, point_y)
    glEnd()
    
def draw_bin():
    # Set bin color to grey and draw the main body of the bin
    glColor3f(0.8, 0.8, 0.8)  # Light grey color
    glBegin(GL_QUADS)
    glVertex2f(bin_x - BIN_SIZE // 2, 50)  # Bottom left corner
    glVertex2f(bin_x + BIN_SIZE // 2, 50)  # Bottom right corner
    glVertex2f(bin_x + BIN_SIZE // 2, 100)  # Top right corner
    glVertex2f(bin_x - BIN_SIZE // 2, 100)  # Top left corner
    glEnd()

    # Draw bin lid with a darker shade of grey
    glColor3f(0.5, 0.5, 0.5)  # Darker grey color for the lid
    glBegin(GL_QUADS)
    glVertex2f(bin_x - BIN_SIZE // 2, 100)  # Left side of the lid, bottom
    glVertex2f(bin_x + BIN_SIZE // 2, 100)  # Right side of the lid, bottom
    glVertex2f(bin_x + BIN_SIZE // 2, 110)  # Right side of the lid, top
    glVertex2f(bin_x - BIN_SIZE // 2, 110)  # Left side of the lid, top
    glEnd()

    # Add details to the bin for a more realistic look
    # Draw a handle on the lid
    glColor3f(0.3, 0.3, 0.3)  # Dark grey for the handle
    glBegin(GL_QUADS)
    glVertex2f(bin_x - 10, 105)  # Left side of the handle
    glVertex2f(bin_x + 10, 105)  # Right side of the handle
    glVertex2f(bin_x + 10, 108)  # Right side of the handle, slightly higher
    glVertex2f(bin_x - 10, 108)  # Left side of the handle, slightly higher
    glEnd()

    # Draw bin wheels
    glColor3f(1, 0.1, 0.1)  # Almost black for the wheels
    draw_circle(bin_x - BIN_SIZE // 2 + 10, 45, 5, (0, 0, 0))  # Left wheel
    draw_circle(bin_x + BIN_SIZE // 2 - 10, 45, 5, (0, 0, 0))  # Right wheel
   
def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    if game_running and not game_over:
        draw_background()
        draw_bin()
        draw_trash()
        draw_clouds()
        background_music.stop()

        # Display score
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(10, WINDOW_HEIGHT - 30)
        score_text = "Score: " + str(score) + "                                                                                                    Lives: " + str(lives)  # Display lives
        for char in score_text:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    elif not game_running:
        render_iamge_background("assets/main.jpg")
        sliding_text()
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(WINDOW_WIDTH // 2 - 150, 30)
        start_message = "Press SPACE to start the game"
        for char in start_message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    else:  # Game over
        render_iamge_background("assets/game_over.jpg")
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2)
        game_over_message = "Game Over"
        for char in game_over_message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
        glRasterPos2i(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50)
        retry_message = "Press 'R' to retry or 'Q' to quit"
        for char in retry_message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    glutSwapBuffers()

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"TrashFall Game")

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    glutDisplayFunc(draw)
    glutKeyboardFunc(keyboard)
    glutTimerFunc(0, update, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
