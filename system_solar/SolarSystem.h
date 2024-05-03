// -------------------------------------------------------------------------
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// -------------------------------------------------------------------------
#ifndef __taller3__SolarSystem__h__
#define __taller3__SolarSystem__h__

#include <string>
#include <vector>
#include <boost/property_tree/ptree.hpp>

/**
 */
class SolarSystem
{
public:
  SolarSystem( const unsigned int& samples = 36 );
  virtual ~SolarSystem( ) = default;

  const float* bounding_box( ) const;

  void load( const std::string& json_fname );
  void reset( );
  void advance_simulation( const unsigned long long& delta );
  void draw( );

protected:
  float m_SimulationBaseTime { 1 };
  float m_SimulationOffset { 0 };
  boost::property_tree::ptree m_Model;
  float m_BBox[ 4 ] { 0 };

  std::vector< float > m_Circle;
};

#endif // __taller3__SolarSystem__h__

// eof - SolarSystem.h
