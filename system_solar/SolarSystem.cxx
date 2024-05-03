// -------------------------------------------------------------------------
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// -------------------------------------------------------------------------

#include "SolarSystem.h"



#include <iostream>



#include <cmath>
#include <fstream>
#include <sstream>
#include <stack>

#ifdef _MSC_VER
#  include <boost/config/compiler/visualc.hpp>
#endif
#include <boost/property_tree/json_parser.hpp>
#include <boost/optional/optional.hpp>

#include <GL/gl.h>

// -------------------------------------------------------------------------
SolarSystem::
SolarSystem( const unsigned int& samples )
{
  float off = 8.0 * std::atan( 1.0 ) / float( samples );
  for( unsigned int i = 0; i < samples; ++i )
  {
    float w = float( i ) * off;
    this->m_Circle.push_back( std::cos( w ) );
    this->m_Circle.push_back( std::sin( w ) );
  } // end for
  this->m_Circle.shrink_to_fit( );
}

// -------------------------------------------------------------------------
const float* SolarSystem::
bounding_box( ) const
{
  return( this->m_BBox );
}

// -------------------------------------------------------------------------
void SolarSystem::
load( const std::string& json_fname )
{
  this->m_Model.clear( );

  // Read file buffer into memory
  std::ifstream json_file( json_fname.c_str( ) );
  std::istringstream json_str(
    std::string( std::istreambuf_iterator< char >{ json_file }, { } )
    );
  json_file.close( );

  // Read JSON data
  boost::property_tree::ptree json;
  boost::property_tree::read_json( json_str, json );

  // Get all information
  using _T = boost::property_tree::ptree;
  using _O = boost::optional< const _T& >;
  using _It = _T::const_iterator;
  std::stack< std::pair< _It, std::string > > q;
  for( _It i = json.begin( ); i != json.end( ); ++i )
    q.push( std::make_pair( i, "" ) );

  while( q.size( ) > 0 )
  {
    _It i = q.top( ).first;
    std::string p = q.top( ).second;
    q.pop( );

    if( i->first == "SimulationBaseTime" )
      this->m_SimulationBaseTime = i->second.get< float >( "" );
    else
    {
      std::string name = ( p + "." + i->first ).substr( 1 );

      // Is this a celestial object?
      _O size_node = i->second.get_child_optional( "size" );
      if( size_node )
      {
        // Get celestial object properties
        _O color_node = i->second.get_child_optional( "color" );
        _O orbit_node = i->second.get_child_optional( "orbit" );
        _O period_node = i->second.get_child_optional( "period" );
        float size = size_node.get( ).get< float >( "" );
        float orbit =
          ( orbit_node )? orbit_node.get( ).get< float >( "" ): 0;
        float period =
          ( period_node )? period_node.get( ).get< float >( "" ): 0;
        float red = 1, green = 1, blue = 1;
        if( color_node )
        {
          std::istringstream color(
            color_node.get( ).get< std::string >( "" )
            );
          color >> red >> green >> blue;
        } // end if

        // Update tree
        this->m_Model.add( name + ".size", size );
        this->m_Model.add( name + ".orbit", orbit );
        this->m_Model.add(
          name + ".frequency",
          ( period == 0 )? float( 0 ): float( 1 ) / period
          );
        this->m_Model.add( name + ".angle", float( 0 ) );
        this->m_Model.add( name + ".red", red );
        this->m_Model.add( name + ".green", green );
        this->m_Model.add( name + ".blue", blue );

        // Add hierarchical children
        _O planets = i->second.get_child_optional( "planets" );
        if( planets )
          for( _It j = planets->begin( ); j != planets->end( ); ++j )
            q.push( std::make_pair( j, p + "." + i->first ) );
        _O satellites = i->second.get_child_optional( "satellites" );
        if( satellites )
          for( _It j = satellites->begin( ); j != satellites->end( ); ++j )
            q.push( std::make_pair( j, p + "." + i->first ) );
      } // end if
    } // end if
  } // end while

  this->reset( );
}

// -------------------------------------------------------------------------
void SolarSystem::
reset( )
{
  using _T = boost::property_tree::ptree;
  using _O = boost::optional< const _T& >;
  using _It = _T::const_iterator;
  std::stack< std::pair< _It, float > > q;
  for( _It i = this->m_Model.begin( ); i != this->m_Model.end( ); ++i )
    q.push( std::make_pair( i, float( 0 ) ) );

  float radius = 0;
  while( q.size( ) > 0 )
  {
    _It i = q.top( ).first;
    float p = q.top( ).second;
    q.pop( );

    if( p > radius )
      radius = p;

    // This object properties
    _It j = i->second.begin( );
    float size = ( j++ )->second.get_value< float >( );
    float orbit = ( j++ )->second.get_value< float >( );
    float frequency = ( j++ )->second.get_value< float >( );
    float angle = ( j++ )->second.get_value< float >( );
    float red = ( j++ )->second.get_value< float >( );
    float green = ( j++ )->second.get_value< float >( );
    float blue = ( j++ )->second.get_value< float >( );

    // Add hierarchical objects
    for( ; j != i->second.end( ); ++j )
      q.push( std::make_pair( j, p + orbit + size ) );
  } // end while
  this->m_BBox[ 0 ] = this->m_BBox[ 1 ] = -radius;
  this->m_BBox[ 2 ] = this->m_BBox[ 3 ] =  radius;
}

// -------------------------------------------------------------------------
void SolarSystem::
advance_simulation( const unsigned long long& delta )
{
  this->m_SimulationOffset =
    float( delta ) / ( this->m_SimulationBaseTime * 1000.0 );
}

// -------------------------------------------------------------------------
void SolarSystem::
draw( )
{
  using _T = boost::property_tree::ptree;
  using _O = boost::optional< const _T& >;
  using _It = _T::iterator;

  // Prepare visualization stack
  std::stack< _It > q;
  for( _It i = this->m_Model.begin( ); i != this->m_Model.end( ); ++i )
  {
    q.push( i );
    glPushMatrix( );
  } // end for

  // Draw following a stack logic
  while( q.size( ) > 0 )
  {
    // Get next object in stack
    _It i = q.top( );
    q.pop( );
    glPopMatrix( );

    // This object's properties
    _It j = i->second.begin( );
    float size = ( j++ )->second.get_value< float >( );
    float orbit = ( j++ )->second.get_value< float >( );
    float frequency = ( j++ )->second.get_value< float >( );
    float angle = j->second.get_value< float >( );
    angle =
      std::fmod(
        angle + ( 360.0 * this->m_SimulationOffset * frequency ), 360.0
        );
    ( j++ )->second.put_value( angle );
    float red = ( j++ )->second.get_value< float >( );
    float green = ( j++ )->second.get_value< float >( );
    float blue = ( j++ )->second.get_value< float >( );

    // Localize object
    glRotatef( angle, 0, 0, 1 );
    glTranslatef( orbit, 0, 0 );

    // Draw object in its local coordinate system
    glPushMatrix( );
    glScalef( size, size, 1 );
    glColor3f( red, green, blue );
    const float* b = this->m_Circle.data( );
    glBegin( GL_POLYGON );
    {
      for( unsigned long long i = 0; i < this->m_Circle.size( ); i += 2 )
        glVertex2fv( b + i );
    }
    glEnd( );
    glPopMatrix( );

    // Add hierarchical (children) objects
    for( ; j != i->second.end( ); ++j )
    {
      q.push( j );
      glPushMatrix( );
    } // end for
  } // end while
}

// eof - SolarSystem.cxx
