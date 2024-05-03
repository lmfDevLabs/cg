// -------------------------------------------------------------------------
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// -------------------------------------------------------------------------

#include <iostream>

#include "Controller.h"
#include "SolarSystem.h"

int main( int argc, char** argv )
{
  if( argc < 2 )
  {
    std::cerr << "Usage: " << argv[ 0 ] << " file.json" << std::endl;
    return( EXIT_FAILURE );
  } // end if

  // Read world
  SolarSystem world( 18 );
  try
  {
    world.load( argv[ 1 ] );
  }
  catch( const std::exception& err )
  {
    std::cerr << "Error caught: " << err.what( ) << std::endl;
    return( EXIT_FAILURE );
  } // end try

  // Configure controller
  Controller controller;
  controller.init( &argc, argv, &world, "Movimiento planetario!", 700, 700 );
  controller.loop( );

  return( EXIT_SUCCESS );
}

// eof - main.cxx
