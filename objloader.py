import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import glm

# Initialize Pygame
pygame.init()

# Set up display
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Set up title
pygame.display.set_caption("3D Model Viewer")

# Load 3D model
def load_model(model_path):
    vertices = []
    faces = []
    with open(model_path, 'r') as f:
        for line in f:
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            if values[0] == 'v':
                v = [float(x) for x in values[1:4]]
                vertices.append(v)
            elif values[0] == 'f':
                face = [int(x.split('/')[0]) for x in values[1:4]]
                faces.append(face)
    return vertices, faces

# Load model
model_path = '20430_Cat_v1_NEW.obj'
vertices, faces = load_model(model_path)

# Load texture
def load_texture(texture_path):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    image = pygame.image.load(texture_path)
    image = pygame.transform.flip(image, False, True)
    image = np.array(image)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.shape[1], image.shape[0], 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture

# Load texture
texture_path = '20430_cat_diff_v1.jpg'
texture = load_texture(texture_path)

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear screen
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    # Draw model
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 5, 0, 0, 0, 0, 1, 0)
    glRotatef(1, 0, 1, 0)

    # Enable texture
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, texture)

    # Draw faces
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_index in face:
            vertex = vertices[vertex_index - 1]
            glVertex3fv(vertex)
    glEnd()

    # Disable texture
    glDisable(GL_TEXTURE_2D)

    # Update display
    pygame.display.flip()
    pygame.time.wait(10)