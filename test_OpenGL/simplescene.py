{"nbformat":4,"nbformat_minor":0,"metadata":{"colab":{"provenance":[],"authorship_tag":"ABX9TyMaC/bg8zXh9tHaev7h0PQX"},"kernelspec":{"name":"python3","display_name":"Python 3"},"language_info":{"name":"python"}},"cells":[{"cell_type":"code","execution_count":1,"metadata":{"colab":{"base_uri":"https://localhost:8080/","height":383},"id":"Uo-oXoJalx8I","executionInfo":{"status":"error","timestamp":1690935201049,"user_tz":300,"elapsed":830,"user":{"displayName":"Carlos Talero","userId":"02343622721106739237"}},"outputId":"9e851642-c172-445f-95b0-beb7e8f95553"},"outputs":[{"output_type":"error","ename":"ValueError","evalue":"ignored","traceback":["\u001b[0;31m---------------------------------------------------------------------------\u001b[0m","\u001b[0;31mValueError\u001b[0m                                Traceback (most recent call last)","\u001b[0;32m<ipython-input-1-f45527cc6527>\u001b[0m in \u001b[0;36m<cell line: 172>\u001b[0;34m()\u001b[0m\n\u001b[1;32m    170\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    171\u001b[0m \u001b[0;31m## -------------------------------------------------------------------------\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 172\u001b[0;31m \u001b[0mglutInit\u001b[0m\u001b[0;34m(\u001b[0m \u001b[0mlen\u001b[0m\u001b[0;34m(\u001b[0m \u001b[0msys\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0margv\u001b[0m \u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0msys\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0margv\u001b[0m \u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m    173\u001b[0m \u001b[0mglutInitDisplayMode\u001b[0m\u001b[0;34m(\u001b[0m \u001b[0mGLUT_RGBA\u001b[0m \u001b[0;34m|\u001b[0m \u001b[0mGLUT_DOUBLE\u001b[0m \u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    174\u001b[0m \u001b[0mmain_window\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0minit\u001b[0m\u001b[0;34m(\u001b[0m \u001b[0;34m'Hola mundo'\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;36m700\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0;36m700\u001b[0m \u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n","\u001b[0;32m/usr/local/lib/python3.10/dist-packages/OpenGL/GLUT/special.py\u001b[0m in \u001b[0;36mglutInit\u001b[0;34m(*args)\u001b[0m\n\u001b[1;32m    307\u001b[0m             \u001b[0mcount\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0marg\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    308\u001b[0m             \u001b[0;32mif\u001b[0m \u001b[0mcount\u001b[0m \u001b[0;34m!=\u001b[0m \u001b[0mlen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m--> 309\u001b[0;31m                 raise ValueError( \"\"\"Specified count of %s does not match length (%s) of argument list %s\"\"\"%(\n\u001b[0m\u001b[1;32m    310\u001b[0m                     \u001b[0mcount\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mlen\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0margs\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0margs\u001b[0m\u001b[0;34m,\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m    311\u001b[0m                 ))\n","\u001b[0;31mValueError\u001b[0m: Specified count of 3 does not match length (1) of argument list (['/usr/local/lib/python3.10/dist-packages/ipykernel_launcher.py', '-f', '/root/.local/share/jupyter/runtime/kernel-cfd57622-821e-4461-a4da-b066fbd2efda.json'],)"]}],"source":["## =========================================================================\n","## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)\n","## =========================================================================\n","## Install OpenGL: pip3 install PyOpenGL PyOpenGL_accelerate\n","## =========================================================================\n","\n","import math, sys\n","from OpenGL.GL import *\n","from OpenGL.GLUT import *\n","\n","## -------------------------------------------------------------------------\n","main_window = None\n","window_width = None\n","window_height = None\n","\n","world_left = -1.5\n","world_right = 1.5\n","world_top = 1.5\n","world_bottom = -1.5\n","\n","## -------------------------------------------------------------------------\n","def base( ):\n","  glBegin( GL_LINES )\n","\n","  glColor3f( 1, 0, 0 )\n","  glVertex2f( -0.1, 0 )\n","  glVertex2f( 1, 0 )\n","\n","  glColor3f( 0, 1, 0 )\n","  glVertex2f( 0, -0.1 )\n","  glVertex2f( 0, 1 )\n","\n","  glEnd( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def square( mode = GL_LINE_LOOP ):\n","  glBegin( mode )\n","\n","  glVertex2f( -0.5, -0.5 )\n","  glVertex2f(  0.5, -0.5 )\n","  glVertex2f(  0.5,  0.5 )\n","  glVertex2f( -0.5,  0.5 )\n","\n","  glEnd( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def circle( mode = GL_LINE_LOOP, samples = 30 ):\n","  off = 8.0 * math.atan( 1 ) / float( samples )\n","  glBegin( mode )\n","  for i in range( samples ):\n","    w = float( i ) * off\n","    glVertex2f( math.cos( w ), math.sin( w ) )\n","  # end for\n","  glEnd( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def triangle( mode = GL_LINE_LOOP ):\n","  glBegin( mode )\n","\n","  glVertex2f( 0, 1 )\n","  glVertex2f( -0.86602540378443, -0.5 )\n","  glVertex2f(  0.86602540378443, -0.5 )\n","\n","  glEnd( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def init( title, width, height ):\n","  global window_width, window_height\n","\n","  window_width = width\n","  window_height = height\n","\n","  glutInitWindowSize( window_width, window_height )\n","  wnd = glutCreateWindow( title )\n","\n","  # Set clear color\n","  glClearColor( 0, 0, 0, 0 )\n","\n","  # Prepare Viewport\n","  glViewport( 0, 0, window_width, window_height )\n","\n","  #\n","  glMatrixMode( GL_PROJECTION )\n","  glLoadIdentity( )\n","\n","  # ???\n","  glMatrixMode( GL_MODELVIEW )\n","  glLoadIdentity( )\n","\n","  return wnd\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def reshape( width, height ):\n","  global window_width, window_height\n","\n","  window_width = width\n","  window_height = height\n","\n","  # Set the viewport to cover the new window\n","  glViewport( 0, 0, window_width, window_height )\n","\n","  # ???\n","  glMatrixMode( GL_PROJECTION )\n","  glLoadIdentity( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def click( button, state, x, y ):\n","  ## print( \"click: \" + str( button ) + ' ' + str( state ) + \" \" + str( x ) + \" \" + str( y ) )\n","  pass\n","  '''\n","  TODO\n","  if( button == GLUT_LEFT_BUTTON && state == GLUT_DOWN )\n","  {\n","  }\n","  '''\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def active_move( x, y ):\n","  ## print( \"active_move: \" + str( x ) + \" \" + str( y ) )\n","  pass\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def passive_move( x, y ):\n","  ## print( \"passive_move: \" + str( x ) + \" \" + str( y ) )\n","  pass\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def keyboard( key, x, y ):\n","  if key == b'\\x1b': # ESC\n","    if not main_window is None:\n","      glutDestroyWindow( main_window )\n","    # end if\n","  # end if\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def draw( ):\n","  global world_left, world_right, world_top, world_bottom\n","\n","  # Clear framebuffer and model transform\n","  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )\n","\n","\n","  glMatrixMode( GL_MODELVIEW )\n","  glLoadIdentity( )\n","\n","\n","\n","\n","  # Base\n","  base( )\n","\n","  # Square\n","  glColor3f( 1, 1, 1 )\n","  square( )\n","\n","  # Prepare next frame\n","  glutSwapBuffers( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","def idle( ):\n","  ## print( 'idle' )\n","  glutPostRedisplay( )\n","# end def\n","\n","## -------------------------------------------------------------------------\n","glutInit( len( sys.argv ), sys.argv )\n","glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE )\n","main_window = init( 'Hola mundo', 700, 700 )\n","\n","# View functions\n","glutReshapeFunc( reshape )\n","glutDisplayFunc( draw )\n","glutIdleFunc( idle )\n","\n","# Interaction functions\n","glutKeyboardFunc( keyboard )\n","glutMouseFunc( click )\n","glutMotionFunc( active_move )\n","glutPassiveMotionFunc( passive_move )\n","\n","# Go!\n","glutMainLoop( )\n","\n","## eof - simple_scene.py\n"]}]}