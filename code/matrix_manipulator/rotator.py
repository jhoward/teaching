"""
rotator.py

Author: James Howard
        Special Thanks to Jeff Molofee and tutorials from NeHe
        
Program used to display the effect of modifying the rotation matricies on 
a torus.
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys

from opengl_init import *       # Draw (), Initialize () and all the real OpenGL work.
from rotation_math import *       # // *NEW* ArcBall header

# Number of the glut window.
window = 0


# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):              # We call this right after our OpenGL window is created.

    glShadeModel(GL_SMOOTH)             # Enables Smooth Color Shading
    glClearColor(0.0, 0.0, 0.0, 0.5)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                   # Enables Clearing Of The Depth Buffer
    glEnable(GL_DEPTH_TEST)             # Enables Depth Testing
    glDepthFunc(GL_LEQUAL)              # The Type Of Depth Test To Do
    glHint (GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST) # Really Nice Perspective Calculations

    return True                                 # // Initialization Went OK


# Reshape The Window When It's Moved Or Resized
def ReSizeGLScene(Width, Height):
    if Height == 0:                     # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)     # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)         # // Select The Projection Matrix
    glLoadIdentity()                    # // Reset The Projection Matrix
    # // field of view, aspect ratio, near and far
    # This will squash and stretch our objects as the window is resized.
    # Note that the near clip plane is 1 (hither) and the far plane is 1000 (yon)
    gluPerspective(45.0, float(Width)/float(Height), 1, 100.0)

    glMatrixMode (GL_MODELVIEW);        # // Select The Modelview Matrix
    glLoadIdentity ();                  # // Reset The Modelview Matrix
    g_ArcBall.setBounds (Width, Height) # //*NEW* Update mouse bounds for arcball
    return


def main():
    global window
    # pass arguments to init
    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    
    # get a 640 x 480 window 
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    
    window = glutCreateWindow("Torus Rotation Window")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(Draw)
    
    # Uncomment this line to get full screen.
    #glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(Draw)
    
    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)
    
    # Register the function called when the keyboard is pressed.  
    glutKeyboardFunc(keyPressed)

    # GLUT When mouse buttons are clicked in window
    glutMouseFunc (Upon_Click)

    # GLUT When the mouse mvoes
    glutMotionFunc (Upon_Drag)


    # We've told Glut the type of window we want, and we've told glut about
    # various functions that we want invoked (idle, resizing, keyboard events).
    # Glut has done the hard work of building up thw windows DC context and 
    # tying in a rendering context, so we are ready to start making immediate mode
    # GL calls.
    # Call to perform inital GL setup (the clear colors, enabling modes
    Initialize (640, 480)

    # Start Event Processing Engine 
    glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
    print "Hit ESC key to quit."
    main()

