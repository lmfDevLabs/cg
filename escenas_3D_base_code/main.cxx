// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <iostream>
#include <string>

#include "Object.h"


int main( int argc, char** argv )
{
  std::string in_fname = argv[ 1 ];

  Object obj;
  obj.read_from_OBJ( in_fname );


  return( EXIT_SUCCESS );
}

// eof - main.cxx
