// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ__Object__h__
#define __PUJ__Object__h__

#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

class Object
{
public:
  Object( )
    {
    }

  virtual ~Object( ) = default;

  void read_from_OBJ( const std::string& in_fname )
    {
      // Read file buffer into memory
      std::ifstream in_file( in_fname.c_str( ) );
      std::istringstream in_str(
        std::string( std::istreambuf_iterator< char >{ in_file }, { } )
        );
      in_file.close( );

      // Prepare internal data
      this->m_Points.clear( );
      this->m_Faces.clear( );

      // Read line by line
      std::string line;
      while( std::getline( in_str, line ) )
      {
        std::istringstream line_str( line );
        std::string cmd;
        line_str >> cmd;
        if( cmd == "v" )
        {
          unsigned int n = 0;
          while( line_str && n < 3 )
          {
            this->m_Points.push_back( 0 );
            line_str >> this->m_Points.back( );
            n++;
          } // end while
        }
        else if( cmd == "f" )
        {
          this->m_Faces.push_back( std::vector< unsigned int >( ) );
          while( line_str )
          {
            this->m_Faces.back( ).push_back( 0 );
            line_str >> this->m_Faces.back( ).back( );
            this->m_Faces.back( ).back( )--;
          } // end while
          this->m_Faces.back( ).pop_back( );
          this->m_Faces.back( ).shrink_to_fit( );
        } // end if
      } // end while

      // Free unused memory
      this->m_Points.shrink_to_fit( );
      this->m_Faces.shrink_to_fit( );
    }

protected:
  std::vector< float > m_Points;
  std::vector< std::vector< unsigned int > > m_Faces;
};

#endif // __PUJ__Object__h__

// eof - Object.h
