// -------------------------------------------------------------------------
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// -------------------------------------------------------------------------
#ifndef __taller3__Controller__h__
#define __taller3__Controller__h__

#include <chrono>
#include <string>

// -- FORWARD DECLARATIONS --
class SolarSystem;

/**
 */
class Controller
{
public:
  using Self = Controller;

public:
  static void init(
    int* argc, char** argv,
    SolarSystem* s, const std::string& t, int w, int h
    );
  static void reshape( int w, int h );
  static void click( int b, int s, int x, int y );
  static void passive_move( int i, int j );
  static void keyboard( unsigned char k, int x, int y );
  static void draw( );
  static void idle( );
  static void timer( int v );
  static void loop( );

protected:
  static void _inv_prj( );

protected:
  static SolarSystem* s_World;

  static int   s_MainWindow;
  static int   s_ViewPort[ 4 ];
  static float s_InvPrj[ 16 ];

  static std::chrono::high_resolution_clock::time_point s_StartTime;
  static bool s_Animating;
};

#endif // __taller3__Controller__h__

// eof - Controller.h
