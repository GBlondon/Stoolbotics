#!/usr/bin/env python
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from config import *
from math import *
import sys
import Image
import numpy
from tools import *

class point():
  def __init__(self, x, y, z, label=""):
    self.x = x
    self.y = y
    self.z = z
    self.label = label

  def draw(self):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex3f(self.x, self.y, self.z)
    glEnd()
    name = self.label
    name += " (" + str(round(self.x, 3)) + ", " + str(round(self.y, 3)) + ", " + str(round(self.z, 3)) + ")"
    text_at_pos(self.x + 1, self.y + 1, self.z + 1, name, GLUT_BITMAP_TIMES_ROMAN_10)

def draw_rotational_joint(cx, cy, cz, r, l): #draws cylinder along z axis
    glTranslate(0,0,-l/2)
    draw_rotational_joint_endCap(r,l/3)
    gluCylinder(gluNewQuadric(), r, r, l, l/3, 1)
    glTranslate(0,0,l)
    draw_rotational_joint_endCap(r,l/3)
    glTranslate(0,0,-l/2)

def draw_rotational_joint_endCap(r, sides):
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0,r/2,0)
    for angle in arange(0, 2*PI, 2*PI/sides):
        glVertex3f(cos(angle)*r, sin(angle)*r,0)
    glVertex3f(r, 0, 0)
    glEnd()

def draw_prismatic_joint(cx, cy, cz, l, w, h):
    glBegin(GL_QUAD_STRIP)
    #Quads 1 2 3 4
    glVertex3f(cx+l/2, cy-w/2, cz-h/2)   #V2
    glVertex3f(cx-l/2, cy-w/2, cz-h/2)   #V1
    glVertex3f(cx+l/2, cy-w/2, cz+h/2)   #V4
    glVertex3f(cx-l/2, cy-w/2, cz+h/2)   #V3
    glVertex3f(cx+l/2, cy+w/2, cz+h/2)   #V6
    glVertex3f(cx-l/2, cy+w/2, cz+h/2)   #V5
    glVertex3f(cx+l/2, cy+w/2, cz-h/2)   #V8
    glVertex3f(cx-l/2, cy+w/2, cz-h/2)   #V7
    glVertex3f(cx+l/2, cy-w/2, cz-h/2)   #V2
    glVertex3f(cx-l/2, cy-w/2, cz-h/2)   #V1
    glEnd()
    
    #Quad 5
    glBegin(GL_QUADS)
    glVertex3f(cx+l/2, cy+w/2, cz-h/2)   #V8
    glVertex3f(cx+l/2, cy+w/2, cz+h/2)   #V6
    glVertex3f(cx+l/2, cy-w/2, cz+h/2)   #V4
    glVertex3f(cx+l/2, cy-w/2, cz-h/2)   #V2
    #Quad 6
    glVertex3f(cx-l/2, cy+w/2, cz-h/2)   #V7
    glVertex3f(cx-l/2, cy+w/2, cz+h/2)   #V5
    glVertex3f(cx-l/2, cy-w/2, cz+h/2)   #V3
    glVertex3f(cx-l/2, cy-w/2, cz-h/2)   #V1
    glEnd()
    
def text_at_pos( x, y, z, text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    glRasterPos3f(x, y, z)
    drawBitmapString(text, font)

def drawBitmapString(text, font=GLUT_BITMAP_TIMES_ROMAN_24):
    for c in text:
        glutBitmapCharacter(font, ord(c))
        
def draw_axes(number=''):
    axes_l = 15
    glBegin(GL_LINES)
    
    # x axis
    glVertex3f(0, 0, 0)
    glVertex3f(axes_l, 0, 0)
    
    glVertex3f(axes_l, 0, 0)
    glVertex3f(axes_l-(axes_l/5), (axes_l/5), 0)
    
    glVertex3f(axes_l, 0, 0)
    glVertex3f(axes_l-(axes_l/5), -(axes_l/5), 0)
    
    # y axis
    glVertex3f(0, 0, 0)
    glVertex3f(0, axes_l, 0)
    
    glVertex3f(0, axes_l, 0)
    glVertex3f(0, axes_l-(axes_l/5), (axes_l/5))

    glVertex3f(0, axes_l, 0)
    glVertex3f(0, axes_l-(axes_l/5), -(axes_l/5))

    # z axis
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, axes_l)

    glVertex3f(0, 0, axes_l)
    glVertex3f(0, (axes_l/5), axes_l-(axes_l/5))

    glVertex3f(0, 0, axes_l)
    glVertex3f(0, -(axes_l/5), axes_l-(axes_l/5))
    
    glEnd()
    
    text_at_pos(axes_l+1, 0, 0, 'x'+number)
    text_at_pos(0, axes_l+1, 0, 'y'+number)
    text_at_pos(0, 0, axes_l+1, 'z'+number)
    
def screendump(self, filename="screendump"):
    s = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
    img = Image.new('RGB', (self.w, self.h))
    img.fromstring(s)
    img2 = img.transpose(Image.FLIP_TOP_BOTTOM)
    img2.save(filename + ".jpg")
    
class gl_window():
    def __init__(self, w=700, h=400):
        self.w = w
        self.h = h
        
        self.step = 0
        
        glutInit([])
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(self.w, self.h)
        glutInitWindowPosition(100, 100) 
        glutCreateWindow(sys.argv[0])
        self.setup()

        glutDisplayFunc(self.draw)
        glutKeyboardFunc(self.keyboard)
        glutReshapeFunc(self.resize)
        self.run()
        
    def run(self):
        glutMainLoop()
  

  
    def keyboard(self, key, x, y):
        if key == chr(27):
            sys.exit(0)
        elif key == 'a':
            self.screendump(str(self.step))
            self.step += 1
        elif key == 's':
            self.screendump()
            
    

    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0.0, 0.0, 0.0)

        glPushMatrix()
        
        # make a right hand coordinate system
        glTranslatef(-10.0, -10.0, -10.0)
        glRotatef(-45, 1.0, 0.0, 0.0)
        glRotatef(-45, 0.0, 0.0, 1.0)
        
        self.draw_axes()
        
        if self.step == 0:
            # step 2
            text_at_pos(-20.0, 0.0, 25.0, "Question 2 - Translate point (1, 1, 1) by (2, 3, 4)")
            # generate transformation matrix 1
            # translate by 2, 3, 4
            T1 = identity(4, float)
            T1[:3, -1:] = array([2, 3, 4]).reshape(3 , 1)
            
            # start out with (1,1,1)
            p = ones((4,1))
            point(p[0][0], p[1][0], p[2][0], "Initial point").draw()
            
            # apply matrix 1, translate by 2, 3, 4
            p = dot(T1, p)
            point(p[0][0], p[1][0], p[2][0], "Translated point").draw()
            glutPostRedisplay()

        elif self.step == 1:
            # step 4
            text_at_pos(-20.0, 0.0, 25.0, "Question 4 - Rotate answer from 2 around the z axis by 90 degrees")
            
            # generate transformation matrix 1
            # translate by 2, 3, 4
            T1 = identity(4, float)
            T1[:3, -1:] = array([2, 3, 4]).reshape(3 , 1)
            
            # start out with (1,1,1)
            p = ones((4,1))
            point(p[0][0], p[1][0], p[2][0], "Initial point").draw()
            
            # apply matrix 1, translate by 2, 3, 4
            p = dot(T1, p)
            point(p[0][0], p[1][0], p[2][0], "Translated point").draw()
            
            # generate second transformatiom matrix 2
            # rotate around z axis
            z = array([[0],[0],[1]])
            theta = 90
            T2 = rot(z, theta, 4);
            
            # apply matrix 2, rotate around z
            p = dot(T2, p)
            point(p[0][0], p[1][0], p[2][0], "Rotated point").draw()
            
            
            glutPostRedisplay()
        elif self.step == 2:
            # step 6
            text_at_pos(-20.0, 0.0, 25.0, "Question 6 - Consolidate matricies from 1 and 3")
            
            # generate transformation matrix 1
            # translate by 2, 3, 4
            T1 = identity(4, float)
            T1[:3, -1:] = array([2, 3, 4]).reshape(3 , 1)
            
            # generate second transformatiom matrix 2
            # rotate around z axis
            z = array([[0],[0],[1]])
            theta = 90
            T2 = rot(z, theta, 4);
            
            # consolidate them into one trans. matrix
            T3 = dot(T2, T1)
            
            # start out with (1,1,1)
            p = ones((4,1))
            point(p[0][0], p[1][0], p[2][0], "Initial point").draw()
            
            # apply matrix 3, translate and rotate all at once
            p = dot(T3, p)
            point(p[0][0], p[1][0], p[2][0], "Translated and rotated point").draw()
            glutPostRedisplay()
        else:
            sys.exit(0)
        glPopMatrix()
        glutSwapBuffers()

    def setup(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)

    def resize(self, _w, _h):
        global w, h
        w = _w
        h = _h
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        #glFrustum(-15.0, 15.0, -15.0, 15.0, 5.0, 1000.0)
        
        glOrtho(-50/2, 50/2, -50/2, 50/2, -50/2, 50/2);
      
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
