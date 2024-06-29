from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *
from settings import *
from graphics import *

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
   