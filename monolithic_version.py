import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
import pygame

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BIN_SIZE = 80
TRASH_SIZE = 20
TRASH_SPEED = 5
CLOUD_SPEED = 2
FLOWER_RADIUS = 5
TREE_HEIGHT = 50
TREE_WIDTH = 20

# Global variables
bin_x = WINDOW_WIDTH // 2
trash_x = random.randint(0, WINDOW_WIDTH)
trash_y = WINDOW_HEIGHT
score = 0
lives = 3
game_over = False
clouds = []
flowers = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT // 4)) for _ in range(10)]
trees = [(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT // 4)) for _ in range(5)]
sliding_text_offset = 1  # Offset for sliding text

# Play background music
pygame.mixer.init()
background_music = pygame.mixer.Sound("background.mp3")
game_over_sound = pygame.mixer.Sound("gameover.mp3")
trash_sound = pygame.mixer.Sound("trash.mp3")
trash2_sound = pygame.mixer.Sound("trash2.mp3")
trash3_sound = pygame.mixer.Sound("trash3.mp3")
collect = pygame.mixer.Sound("collect.mp3")
yay = pygame.mixer.Sound("yay.mp3")
background_music.set_volume(0.5)
background_music.play(-1)

# Variable to track if the game is running
game_running = False

def draw_circle(x, y, radius, color):
    glColor3fv(color)
    sides = 32
    glBegin(GL_TRIANGLE_FAN)
    for i in range(sides + 1):
        cosine = radius * cos(i * 2 * pi / sides) + x
        sine = radius * sin(i * 2 * pi / sides) + y
        glVertex2f(cosine, sine)
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

def draw_sky():
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.7, 1.0)  # Light blue color for the top of the sky
    glVertex2f(0, WINDOW_HEIGHT)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
    glColor3f(0.2, 0.4, 0.8)  # Dark blue color for the bottom of the sky
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT / 2)
    glVertex2f(0, WINDOW_HEIGHT / 2)
    glEnd()

def draw_grass():
    glBegin(GL_QUADS)
    glColor3f(0.0, 0.6, 0.0)  # Green color for the grass
    glVertex2f(0, 0)
    glVertex2f(WINDOW_WIDTH, 0)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT / 2)
    glVertex2f(0, WINDOW_HEIGHT / 2)
    glEnd()

    # Add small grass at the bottom
    glColor3f(0.0, 0.4, 0.0)  # Darker green color for small grass
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WINDOW_WIDTH, 0)
    glVertex2f(WINDOW_WIDTH, 10)  # Height of small grass
    glVertex2f(0, 30)  # Height of small grass
    glEnd()

def draw_flowers():
    for flower_x, flower_y in flowers:
        draw_circle(flower_x, flower_y, FLOWER_RADIUS, (1, 0, 0))  # Red flowers

def draw_trees():
    for tree_x, tree_y in trees:
        # Tree trunk
        glColor3f(0.55, 0.27, 0.07)  # Brown color for the trunk
        glBegin(GL_QUADS)
        glVertex2f(tree_x, tree_y)
        glVertex2f(tree_x + TREE_WIDTH, tree_y)
        glVertex2f(tree_x + TREE_WIDTH, tree_y + TREE_HEIGHT)
        glVertex2f(tree_x, tree_y + TREE_HEIGHT)
        glEnd()
        # Tree foliage
        draw_circle(tree_x + TREE_WIDTH // 2, tree_y + TREE_HEIGHT, TREE_HEIGHT // 2.5, (0, 0.5, 0))  # Green foliage

def draw_building(x, y, z, width, height, depth, color):
    # Define the vertices of the building
    vertices = [
        (x, y, z),  # Front bottom left
        (x + width, y, z),  # Front bottom right
        (x + width, y + height, z),  # Front top right
        (x, y + height, z),  # Front top left
        (x, y, z + depth),  # Back bottom left
        (x + width, y, z + depth),  # Back bottom right
        (x + width, y + height, z + depth),  # Back top right
        (x, y + height, z + depth)  # Back top left
    ]
    
    # Define the faces of the building using indices of the vertices
    faces = [
        (0, 1, 2, 3),  # Front face
        (4, 5, 6, 7),  # Back face
        (0, 3, 7, 4),  # Left face
        (1, 2, 6, 5),  # Right face
        (3, 2, 6, 7),  # Top face
        (0, 1, 5, 4)  # Bottom face
    ]
    
    # Set color and draw each face
    glColor3fv(color)
    glBegin(GL_QUADS)
    for face in faces:
        for vertex_index in face:
            glVertex3fv(vertices[vertex_index])
    glEnd()

def draw_skyline():
    # Draw buildings
    buildings = [
        (100, 200, 0, 30, 150, 20, (0.5, 0.5, 1.0)),  # x, y, z, width, height, depth, color
        (150, 150, 0, 40, 200, 20, (0.4, 0.4, 1.0)),
        (250, 180, 0, 30, 170, 20, (0.6, 0.6, 1.0)),
        (300, 220, 0, 35, 130, 20, (0.7, 0.7, 1.0)),
        (400, 170, 0, 45, 240, 20, (0.45, 0.45, 1.0)),
        (500, 190, 0, 37, 130, 20, (0.55, 0.55, 1.0)),
    (550, 160, 0, 30, 145, 20, (0.5, 0.5, 1.0)),
        (600, 200, 0, 50, 180, 20, (0.5, 0.5, 1.0)),
        (650, 150, 0, 40, 220, 20, (0.4, 0.4, 1.0)),
        (700, 180, 0, 30, 170, 20, (0.6, 0.6, 1.0)),
        (750, 220, 0, 35, 130, 20, (0.7, 0.7, 1.0))
    ]
    
    for building in buildings:
        draw_building(*building)

def draw_sky():
    # Draw the sky background
    glBegin(GL_QUADS)
    glColor3f(0.5, 0.7, 1.0)  # Light blue color for the sky
    glVertex2f(0, WINDOW_HEIGHT)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT)
    glVertex2f(WINDOW_WIDTH, WINDOW_HEIGHT / 2)
    glVertex2f(0, WINDOW_HEIGHT / 2)
    glEnd()

def draw_wooden_bench(x, y, width, height, leg_height, color_seat, color_legs):
    # Draw bench seat
    glColor3fv(color_seat)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    # Draw bench legs
    leg_width = width / 10  # Adjust leg width relative to bench seat width
    glColor3fv(color_legs)
    glBegin(GL_QUADS)
    glVertex2f(x - leg_width, y)
    glVertex2f(x, y)
    glVertex2f(x, y + leg_height)
    glVertex2f(x - leg_width, y + leg_height)

    glVertex2f(x + width, y)
    glVertex2f(x + width + leg_width, y)
    glVertex2f(x + width + leg_width, y + leg_height)
    glVertex2f(x + width, y + leg_height)
    glEnd()

    # Draw additional support for bench legs
    support_width = leg_width / 2
    glColor3fv(color_legs)
    glBegin(GL_QUADS)
    glVertex2f(x - leg_width, y - leg_height / 2)
    glVertex2f(x, y - leg_height / 2)
    glVertex2f(x, y)
    glVertex2f(x - leg_width, y)

    glVertex2f(x + width, y - leg_height / 2)
    glVertex2f(x + width + leg_width, y - leg_height / 2)
    glVertex2f(x + width + leg_width, y)
    glVertex2f(x + width, y)
    glEnd()

def draw_background():
    draw_sky()
    draw_skyline()
    draw_grass()
    draw_flowers()
    draw_trees()
    draw_wooden_bench(100, 150, 150, 20, 50, (0.4, 0.2, 0.0), (0.3, 0.15, 0.0))  # First bench
    draw_wooden_bench(500, 150, 150, 20, 50, (0.4, 0.2, 0.0), (0.3, 0.15, 0.0))  # Second bench

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

def draw_semicircle(radius, num_segments, pos, color, offset=0):
    glColor3fv(color)
    glBegin(GL_POLYGON)
    for i in range(num_segments // 2 + 1):  # Half the number of segments for a semicircle
        angle = pi * i / (num_segments // 2)  # Pi radians for a half circle
        angle += offset
        x = pos[0] + radius * cos(angle)
        y = pos[1] + radius * sin(angle)
        glVertex2f(x, y)
    glEnd()
    
def draw_clouds():
    # Draw clouds with a semi-circle and a few circles
    global clouds
    for cloud in clouds:
        draw_semicircle(cloud[2], 32, (cloud[0], cloud[1]), (1, 1, 1))
        draw_semicircle(cloud[2] * 0.8, 32, (cloud[0] - cloud[2] / 2, cloud[1]), (1, 1, 1))
        draw_semicircle(cloud[2] * 0.8, 32, (cloud[0] + cloud[2] / 2, cloud[1]), (1, 1, 1))
        # inversed semi-circle
        cloud[0] += CLOUD_SPEED
        if cloud[0] > WINDOW_WIDTH + cloud[2] / 2:
            cloud[0] = -cloud[2] / 2
    
    # Add new cloud if needed
    if len(clouds) == 0 or clouds[-1][0] > WINDOW_WIDTH / 2:    
        clouds.append([-50, random.randint(WINDOW_HEIGHT // 2, WINDOW_HEIGHT), random.randint(20, 50)])
    
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
        render_iamge_background("main.jpg")
        sliding_text()
        glColor3f(1.0, 1.0, 1.0)
        glRasterPos2i(WINDOW_WIDTH // 2 - 150, 30)
        start_message = "Press SPACE to start the game"
        for char in start_message:
            glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

    else:  # Game over
        render_iamge_background("game_over.jpg")
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
    glutCreateWindow(b"Trash Collector Game")

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
