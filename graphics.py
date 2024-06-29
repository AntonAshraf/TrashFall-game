from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import *

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
    
    
def draw_circle(x, y, radius, color):
    glColor3fv(color)
    sides = 32
    glBegin(GL_TRIANGLE_FAN)
    for i in range(sides + 1):
        cosine = radius * cos(i * 2 * pi / sides) + x
        sine = radius * sin(i * 2 * pi / sides) + y
        glVertex2f(cosine, sine)
    glEnd()
