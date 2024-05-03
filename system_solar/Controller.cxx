// -------------------------------------------------------------------------
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// -------------------------------------------------------------------------

#include "Controller.h"
#include "SolarSystem.h"

#include <GL/gl.h>
#include <GL/glut.h>

// -------------------------------------------------------------------------
SolarSystem* Controller::s_World         { nullptr };
int          Controller::s_MainWindow    { 0 };
int          Controller::s_ViewPort[ 4 ] { 0 };
float        Controller::s_InvPrj[ 16 ]  { 0 };
std::chrono::high_resolution_clock::time_point Controller::s_StartTime;
bool Controller::s_Animating { false };

// -------------------------------------------------------------------------
void Controller::
init(
  int* argc, char** argv, SolarSystem* s, const std::string& t, int w, int h
  )
{
  // Associate world
  Self::s_World = s;

  // Configure GLUT
  glutInit( argc, argv );
  glutInitDisplayMode( GLUT_RGBA | GLUT_DOUBLE );

  // Register window
  glutInitWindowSize( w, h );
  Self::s_MainWindow = glutCreateWindow( t.c_str( ) );

  // Clear all rendering objects
  glClearColor( 0, 0, 0, 0 );
  Controller::reshape( w, h );
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  // Register events
  glutReshapeFunc( Controller::reshape );
  glutMouseFunc( Controller::click );
  glutPassiveMotionFunc( Controller::passive_move );
  glutKeyboardFunc( Controller::keyboard );
  glutDisplayFunc( Controller::draw );
  glutIdleFunc( Controller::idle );
}

// -------------------------------------------------------------------------
void Controller::
reshape( int w, int h )
{
  // Set the viewport to cover the new window size
  Self::s_ViewPort[ 0 ] = 0;
  Self::s_ViewPort[ 1 ] = 0;
  Self::s_ViewPort[ 2 ] = w;
  Self::s_ViewPort[ 3 ] = h;
  glViewport(
    Self::s_ViewPort[ 0 ],
    Self::s_ViewPort[ 1 ],
    Self::s_ViewPort[ 2 ],
    Self::s_ViewPort[ 3 ]
    );

  // Compute projection matrix: aspect
  float vw = float( Self::s_ViewPort[ 2 ] - Self::s_ViewPort[ 0 ] );
  float vh = float( Self::s_ViewPort[ 3 ] - Self::s_ViewPort[ 1 ] );
  float aw = ( vw < vh )? 1: ( vw / ( ( vh != 0 )? vh: 1 ) );
  float ah = ( vh < vw )? 1: ( vh / ( ( vw != 0 )? vw: 1 ) );

  // Compute projection matrix: un-normalized scene size
  float off = 1.01;
  const float* bbox = Self::s_World->bounding_box( );
  float dx = bbox[ 2 ] - bbox[ 0 ];
  float dy = bbox[ 3 ] - bbox[ 1 ];
  float s = 2.0 / ( off * ( ( dx < dy )? dy: dx ) );

  // Reset world-to-viewport transformation
  glMatrixMode( GL_PROJECTION );
  glLoadIdentity( );
  glScalef( s / aw, s / ah, 1.0 );

  // Prepare retro-projection matrix (pickup points)
  glGetFloatv( GL_PROJECTION_MATRIX, Self::s_InvPrj );
  Controller::_inv_prj( );
  Self::s_InvPrj[  3 ] += Self::s_InvPrj[ 1 ] - Self::s_InvPrj[ 0 ];
  Self::s_InvPrj[  7 ] += Self::s_InvPrj[ 5 ] - Self::s_InvPrj[ 4 ];
  Self::s_InvPrj[ 11 ] += Self::s_InvPrj[ 9 ] - Self::s_InvPrj[ 8 ];
  Self::s_InvPrj[ 0 ] *=  2.0 / vw;
  Self::s_InvPrj[ 4 ] *=  2.0 / vw;
  Self::s_InvPrj[ 8 ] *=  2.0 / vw;
  Self::s_InvPrj[ 1 ] *= -2.0 / vh;
  Self::s_InvPrj[ 5 ] *= -2.0 / vh;
  Self::s_InvPrj[ 9 ] *= -2.0 / vh;
}

// -------------------------------------------------------------------------
void Controller::
click( int b, int s, int x, int y )
{
}

// -------------------------------------------------------------------------
void Controller::
passive_move( int i, int j )
{
}

// -------------------------------------------------------------------------
void Controller::
keyboard( unsigned char k, int x, int y )
{
  if( k == '+' )
  {
    if( !Self::s_Animating )
    {
      Self::s_Animating = true;
      glutTimerFunc( 20, Self::timer, 1 );
    } // end if
  }
  else if( k == '-' )
  {
    Self::s_Animating = false;
    glutTimerFunc( 20, Self::timer, 0 );
  }
  else if( k == 27 /*ESC*/ )
    if( Self::s_MainWindow != 0 )
      glutDestroyWindow( Self::s_MainWindow );
}

// -------------------------------------------------------------------------
void Controller::
draw( )
{
  // Clear framebuffer and model transform
  glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT );
  glMatrixMode( GL_MODELVIEW );
  glLoadIdentity( );

  // Prepare next frame
  if( Self::s_World != nullptr )
    Self::s_World->draw( );
  glutSwapBuffers( );
}

// -------------------------------------------------------------------------
void Controller::
timer( int v )
{
  using _R = std::chrono::milliseconds;

  if( Self::s_Animating )
  {
    if( v == 1 )
      Self::s_StartTime = std::chrono::high_resolution_clock::now( );
    unsigned long long d =
      std::chrono::duration_cast< _R >(
        std::chrono::high_resolution_clock::now( ) - Self::s_StartTime
        ).count( );
    Self::s_World->advance_simulation( d );
    glutPostRedisplay( );
    Self::s_StartTime = std::chrono::high_resolution_clock::now( );
    glutTimerFunc( 20, Controller::timer, 0 );
  }
  else
  {
    Self::s_World->advance_simulation( 0 );
    glutPostRedisplay( );
  } // end if
}

// -------------------------------------------------------------------------
void Controller::
idle( )
{
  glutPostRedisplay( );
}

// -------------------------------------------------------------------------
void Controller::
loop( )
{
  glutMainLoop( );
}

// -------------------------------------------------------------------------
void Controller::
_inv_prj( )
{
  float inv[ 16 ] { 0 }, det;
  int i;

  inv[ 0 ] =  Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 10 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 14 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 7 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 14 ] - Self::s_InvPrj[ 7 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 10 ];
  inv[ 1 ] = -Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 10 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 14 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 14 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 10 ];
  inv[ 2 ] =  Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 14 ] * Self::s_InvPrj[ 7 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 7 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 14 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 6 ];
  inv[ 3 ] = -Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 10 ] * Self::s_InvPrj[ 7 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 7 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 10 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 6 ];
  inv[ 4 ] = -Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 10 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 14 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 7 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 14 ] + Self::s_InvPrj[ 7 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 10 ];
  inv[ 5 ] =  Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 10 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 14 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 14 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 10 ];
  inv[ 6 ] = -Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 14 ] * Self::s_InvPrj[ 7 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 7 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 14 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 6 ];
  inv[ 7 ] =  Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 10 ] * Self::s_InvPrj[ 7 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 7 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 10 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 6 ];
  inv[ 8 ] =  Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 7 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 13 ] - Self::s_InvPrj[ 7 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 9 ];
  inv[ 9 ] = -Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 13 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 9 ];
  inv[ 10 ] =  Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 15 ] - Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 7 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 15 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 7 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 13 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 5 ];
  inv[ 11 ] = -Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 11 ] + Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 7 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 11 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 7 ] - Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 9 ] + Self::s_InvPrj[ 3 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 5 ];
  inv[ 12 ] = -Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 14 ] + Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 10 ] + Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 14 ] - Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 10 ] - Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 13 ] + Self::s_InvPrj[ 6 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 9 ];
  inv[ 13 ] =  Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 14 ] - Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 10 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 14 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 10 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 13 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 9 ];
  inv[ 14 ] = -Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 14 ] + Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 13 ] * Self::s_InvPrj[ 6 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 14 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 6 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 13 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 12 ] * Self::s_InvPrj[ 5 ];
  inv[ 15 ] =  Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 5 ] * Self::s_InvPrj[ 10 ] - Self::s_InvPrj[ 0 ] * Self::s_InvPrj[ 9 ] * Self::s_InvPrj[ 6 ] - Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 10 ] + Self::s_InvPrj[ 1 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 6 ] + Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 4 ] * Self::s_InvPrj[ 9 ] - Self::s_InvPrj[ 2 ] * Self::s_InvPrj[ 8 ] * Self::s_InvPrj[ 5 ];

  det = Self::s_InvPrj[ 0 ] * inv[ 0 ] + Self::s_InvPrj[ 4 ] * inv[ 1 ] + Self::s_InvPrj[ 8 ] * inv[ 2 ] + Self::s_InvPrj[ 12 ] * inv[ 3 ];
  if( det != float( 0 ) )
  {
    det = float( 1.0 ) / det;
    for( i = 0; i < 16; i++ )
      Self::s_InvPrj[ i ] = inv[ i ] * det;
  } // end if
}

// eof - Controller.cxx
