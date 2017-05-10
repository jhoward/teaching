from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import copy
from math import cos, sin
import math
from rotation_math import *
import numpy


PI2 = math.pi * 2.0
theta = 10
rad = math.pi/180 * theta

g_Transform = Matrix4fT ()
g_LastRot = Matrix3fT ()
g_ThisRot = Matrix3fT ()

g_ArcBall = ArcBallT (640, 480)
g_isDragging = False
g_quadratic = None
zoomlevel = 4

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'


def xRotation(theta):
    tmp = Matrix3fT()
    
    tmp[1, 1] = cos(theta)
    tmp[1, 2] = sin(theta)
    tmp[2, 1] = -1 * sin(theta)
    tmp[2, 2] = cos(theta)
    
    return tmp
    

def yRotation(theta):
    tmp = Matrix3fT()

    tmp[0, 0] = cos(theta)
    tmp[0, 2] = sin(theta)
    tmp[2, 0] = -1 * sin(theta)
    tmp[2, 2] = cos(theta)

    return tmp


def zRotation(theta):
    tmp = Matrix3fT()

    tmp[0, 0] = cos(theta)
    tmp[0, 1] = sin(theta)
    tmp[1, 0] = -1 * sin(theta)
    tmp[1, 1] = cos(theta)

    return tmp

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def Initialize (Width, Height):             # We call this right after our OpenGL window is created.
    global g_quadratic

    glClearColor(0.0, 0.0, 0.0, 1.0)                    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                                   # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LEQUAL)                              # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                             # Enables Depth Testing
    glShadeModel (GL_FLAT);                             # Select Flat Shading (Nice Definition Of Objects)
    glHint (GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # Really Nice Perspective Calculations

    g_quadratic = gluNewQuadric();
    gluQuadricNormals(g_quadratic, GLU_SMOOTH);
    gluQuadricDrawStyle(g_quadratic, GLU_FILL); 
    # Why? this tutorial never maps any textures?! ? 
    # gluQuadricTexture(g_quadratic, GL_TRUE);          # // Create Texture Coords

    glEnable (GL_LIGHT0)
    glEnable (GL_LIGHTING)

    glEnable (GL_COLOR_MATERIAL)

    return True




def Upon_Drag (cursor_x, cursor_y):
    """ Mouse cursor is moving
        Glut calls this function (when mouse button is down)
        and pases the mouse cursor postion in window coords as the mouse moves.
    """
    global g_isDragging, g_LastRot, g_Transform, g_ThisRot

    if (g_isDragging):
        mouse_pt = Point2fT (cursor_x, cursor_y)
        ThisQuat = g_ArcBall.drag (mouse_pt)                        # // Update End Vector And Get Rotation As Quaternion
        g_ThisRot = Matrix3fSetRotationFromQuat4f (ThisQuat)        # // Convert Quaternion Into Matrix3fT
        # Use correct Linear Algebra matrix multiplication C = A * B
        g_ThisRot = Matrix3fMulMatrix3f (g_LastRot, g_ThisRot)      # // Accumulate Last Rotation Into This One
        g_Transform = Matrix4fSetRotationFromMatrix3f (g_Transform, g_ThisRot)  # // Set Our Final Transform's Rotation From This One
        #print g_ThisRot
        printMatrix()
    return

def Upon_Click (button, button_state, cursor_x, cursor_y):
    """ Mouse button clicked.
        Glut calls this function when a mouse button is
        clicked or released.
    """
    global g_isDragging, g_LastRot, g_Transform, g_ThisRot

    g_isDragging = False
    if (button == GLUT_RIGHT_BUTTON and button_state == GLUT_UP):
        # Right button click
        g_LastRot = Matrix3fSetIdentity ();                         # // Reset Rotation
        g_ThisRot = Matrix3fSetIdentity ();                         # // Reset Rotation
        g_Transform = Matrix4fSetRotationFromMatrix3f (g_Transform, g_ThisRot); # // Reset Rotation
    elif (button == GLUT_LEFT_BUTTON and button_state == GLUT_UP):
        # Left button released
        g_LastRot = copy.copy (g_ThisRot);                          # // Set Last Static Rotation To Last Dynamic One
    elif (button == GLUT_LEFT_BUTTON and button_state == GLUT_DOWN):
        # Left button clicked down
        g_isDragging = True                                         # // Prepare For Dragging
        mouse_pt = Point2fT (cursor_x, cursor_y)
        g_ArcBall.click (mouse_pt);                             # // Update Start Vector And Prepare For Dragging
    return


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
    global g_quadratic, g_Transform, g_LastRot, zoomlevel
    # If escape is pressed, kill everything.
    key = args [0]
    if key == ESCAPE:
        gluDeleteQuadric (g_quadratic)
        sys.exit ()
    
    if key == 'a':
        g_LastRot = Matrix3fMulMatrix3f(g_LastRot, zRotation(rad))
    if key == 'd':
        g_LastRot = Matrix3fMulMatrix3f(g_LastRot, zRotation(-1 * rad))
    if key == 'w':
        g_LastRot = Matrix3fMulMatrix3f(g_LastRot, xRotation(rad))
    if key == 's':
        g_LastRot = Matrix3fMulMatrix3f(g_LastRot, xRotation(-1 * rad))
        
    if key == 'q':
        g_LastRot = Matrix3fMulMatrix3f(g_LastRot, yRotation(rad))
    if key == 'e':
        g_LastRot = Matrix3fMulMatrix3f(g_LastRot, yRotation(-1 * rad))
        
    if key == '+':
        zoomlevel -= 1
    if key == '-':
        zoomlevel += 1
    
    g_Transform = Matrix4fSetRotationFromMatrix3f (g_Transform, g_LastRot);
    printMatrix()
    #print g_Transform


def Torus(MinorRadius, MajorRadius):        
    # // Draw A Torus With Normals
    glBegin( GL_TRIANGLE_STRIP );               # // Start A Triangle Strip
    for i in xrange (20):                       # // Stacks
        for j in xrange (-1, 20):               # // Slices
            # NOTE, python's definition of modulus for negative numbers returns
            # results different than C's
            #       (a / d)*d  +  a % d = a
            if (j < 0):
                wrapFrac = (-j%20)/20.0
                wrapFrac *= -1.0
            else:
                wrapFrac = (j%20)/20.0;
            phi = PI2*wrapFrac;
            sinphi = sin(phi);
            cosphi = cos(phi);

            r = MajorRadius + MinorRadius*cosphi;

            glNormal3f (sin(PI2*(i%20+wrapFrac)/20.0)*cosphi, sinphi, cos(PI2*(i%20+wrapFrac)/20.0)*cosphi);
            glVertex3f (sin(PI2*(i%20+wrapFrac)/20.0)*r, MinorRadius*sinphi, cos(PI2*(i%20+wrapFrac)/20.0)*r);

            glNormal3f (sin(PI2*(i+1%20+wrapFrac)/20.0)*cosphi, sinphi, cos(PI2*(i+1%20+wrapFrac)/20.0)*cosphi);
            glVertex3f (sin(PI2*(i+1%20+wrapFrac)/20.0)*r, MinorRadius*sinphi, cos(PI2*(i+1%20+wrapFrac)/20.0)*r);
    glEnd();                                                        # // Done Torus
    return

def drawAxis():
    glBegin(GL_LINES)
    glVertex3f(-100, 0, 0)
    glVertex3f(100, 0, 0)
    glVertex3f(0, -100, 0)
    glVertex3f(0, 100, 0)
    glVertex3f(0, 0, -100)
    glVertex3f(0, 0, 100)
    glEnd()
    

def unitTriangle(size = 4, offsetx = 1, offsety = 1):
    
    glBegin(GL_LINES)
    glVertex3f(0 + offsetx, 0 + offsety, 0)
    glVertex3f(1 * size + offsetx, 0 + offsety, 0)
    glVertex3f(0 + offsetx, 0 + offsety, 0)
    glVertex3f(.5 * size + offsetx, 1 * size + offsety, 0)
    glVertex3f(1 * size + offsetx, 0 + offsety, 0)
    glVertex3f(.5 * size + offsetx, 1 * size + offsety, 0)
    glEnd()


def function():
    points = []
    
    start = 0
    end = 3
    dist = abs(end - start)
    for i in range(100):
        x = start + dist/99.0 * i
        points.append((x, 2*x - 2, 0))
        
    glBegin(GL_LINE_STRIP)
    for coord in points:
            glVertex3f(coord[0], coord[1], coord[2])
    glEnd()


def printMatrix():
    
    print "%.2f, %.2f" % (g_Transform[0, 0], g_Transform[1, 0])
    print "%.2f, %.2f" % (g_Transform[1, 0], g_Transform[0, 1])
    print ""

def Draw ():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);             # // Clear Screen And Depth Buffer
    glLoadIdentity();                                               # // Reset The Current Modelview Matrix

    
    glTranslatef(0, 0, -1 * zoomlevel);                                    
    
    drawAxis()

    glPushMatrix();                                                 # // NEW: Prepare Dynamic Transform
    glMultMatrixf(g_Transform);                                     # // NEW: Apply Dynamic Transform
    
    #drawAxis()
    
    glColor3f(1.0,0.75,0.75);
    #glutWireTeapot(1.0)
    #Torus(0.2, 1)
    function()
    #unitTriangle()
    glPopMatrix();                                                  # // NEW: Unapply Dynamic Transform

    glFlush ();                                                     # // Flush The GL Rendering Pipeline
    glutSwapBuffers()
    return

