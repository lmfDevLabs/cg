// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
// This example could be used as an introductory example of the complexity
// on computer graphics implementations.
// =========================================================================
// Compilation: g++ -std=c++17 fill_boxes.cxx -o fill_boxes
// =========================================================================
// ./fill_boxes out_cxx.ppm 2560 2048 50 50 50 50 50
// real    0m2.956s
// user    0m2.851s
// sys     0m0.105s
// =========================================================================

#include <cstring>
#include <fstream>
#include <iostream>
#include <random>
#include <sstream>
#include <string>
#include <vector>
#include <tuple>

// -------------------------------------------------------------------------
using TPixel   = unsigned char;
using TNatural = unsigned short;
using TBuffer  = std::tuple< TPixel*, TNatural, TNatural >;

// -------------------------------------------------------------------------
TBuffer CreateFB( const TNatural& w, const TNatural& h );
void ClearFB( TBuffer& B, const TPixel& r, const TPixel& g, const TPixel& b );
const TPixel* Pixel(
  const TBuffer& B,
  const TNatural& i, const TNatural& j
  );
void DrawPixel(
  TBuffer& B,
  const TNatural& i, const TNatural& j,
  const TPixel& r, const TPixel& g, const TPixel& b
  );
void DumpFB( const TBuffer& B, const std::string& fname );
void FreeFB( TBuffer& B );

// -------------------------------------------------------------------------
int main( int argc, char** argv )
{
  if( argc < 4 )
  {
    std::cerr
      << "Usage: " << argv[ 0 ]
      << " out.ppm w h p2 p3 p4 ... pn"
      << std::endl;
    return( EXIT_FAILURE );
  } // end if

  // Get input parameters
  std::string out_fname = argv[ 1 ];
  std::vector< std::tuple< int, int, float > > boxes;
  boxes.push_back(
    std::make_tuple( std::atoi( argv[ 2 ] ), std::atoi( argv[ 3 ] ), 100.0 )
    );
  for( int i = 4; i < argc; ++i )
  {
    float p = std::atof( argv[ i ] ) / 100.0;
    int w = int( float( std::get< 0 >( boxes.back( ) ) ) * p );
    int h = int( float( std::get< 1 >( boxes.back( ) ) ) * p );
    float s = std::get< 2 >( boxes.back( ) ) * p;
    boxes.push_back( std::make_tuple( w, h, s ) );
  } // end for

  // Create initial framebuffer
  TBuffer B =
    CreateFB(
      std::get< 0 >( boxes[ 0 ] ),
      std::get< 1 >( boxes[ 0 ] )
      );

  // Prepare random filling
  std::random_device dev { };
  std::mt19937 gen { dev( ) };
  float M[] = { 127, 127, 127 };
  for( const auto& b: boxes )
  {
    int W = std::get< 0 >( b );
    int H = std::get< 1 >( b );
    float S = std::get< 2 >( b );

    std::normal_distribution< float > dr { M[ 0 ], S };
    std::normal_distribution< float > dg { M[ 1 ], S };
    std::normal_distribution< float > db { M[ 2 ], S };

    for( int w = 0; w < W; ++w )
    {
      for( int h = 0; h < H; ++h )
      {
        float r = dr( gen );
        float g = dg( gen );
        float b = db( gen );

        if( r < 0 ) r = 0;
        if( g < 0 ) g = 0;
        if( b < 0 ) b = 0;
        if( r > 255 ) r = 255;
        if( g > 255 ) g = 255;
        if( b > 255 ) b = 255;

        DrawPixel( B, w, h, TPixel( r ), TPixel( g ), TPixel( b ) );
      } // end for
    } // end for
  } // end for

  // Save image
  DumpFB( B, out_fname );

  // Free memory
  FreeFB( B );

  return( EXIT_SUCCESS );
}

// -------------------------------------------------------------------------
TBuffer CreateFB( const TNatural& w, const TNatural& h )
{
  TBuffer B = std::make_tuple( new TPixel[ w * h * 3 ], w, h );
  std::memset( std::get< 0 >( B ), 0, w * h * 3 * sizeof( TPixel ) );
  return( B );
}

// -------------------------------------------------------------------------
void ClearFB(
  TBuffer& B,
  const TPixel& r, const TPixel& g, const TPixel& b
  )
{
}

// -------------------------------------------------------------------------
const TPixel* Pixel(
  const TBuffer& B,
  const TNatural& i, const TNatural& j
  )
{
  unsigned long long k = 3 * ( ( j * std::get< 1 >( B ) ) + i );
  return( std::get< 0 >( B ) + k );
}

// -------------------------------------------------------------------------
void DrawPixel(
  TBuffer& B,
  const TNatural& i, const TNatural& j,
  const TPixel& r, const TPixel& g, const TPixel& b
  )
{
  unsigned long long k = 3 * ( ( j * std::get< 1 >( B ) ) + i );
  std::get< 0 >( B )[ k ]     = r;
  std::get< 0 >( B )[ k + 1 ] = g;
  std::get< 0 >( B )[ k + 2 ] = b;
}

// -------------------------------------------------------------------------
void DumpFB( const TBuffer& B, const std::string& fname )
{
  std::stringstream out;
  out << "P3" << std::endl;
  out
    << std::get< 1 >( B ) << " "
    << std::get< 2 >( B ) << std::endl
    << "255"
    << std::endl;

  for( int h = 0; h < std::get< 2 >( B ); ++h )
  {
    for( int w = 0; w < std::get< 1 >( B ); ++w )
    {
      const TPixel* p = Pixel( B, w, h );
      out
        << int( p[ 0 ] ) << " "
        << int( p[ 1 ] ) << " "
        << int( p[ 2 ] ) << " ";
    } // end for
    out << std::endl;
  } // end for

  std::ofstream outf( fname );
  outf << out.str( );
  outf.close( );
}

// -------------------------------------------------------------------------
void FreeFB( TBuffer& B )
{
  delete [] std::get< 0 >( B );
}

// eof - fill_boxes.cxx
