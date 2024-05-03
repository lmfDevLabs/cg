// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================

#include <PUJ_CGraf/AmbientLight.h>

#include <GL/gl.h>

// -------------------------------------------------------------------------
PUJ_CGraf::AmbientLight::
AmbientLight( )
  : Superclass( )
{
}

// -------------------------------------------------------------------------
void PUJ_CGraf::AmbientLight::
set_color( const TReal& r, const TReal& g, const TReal& b, const TReal& a )
{
  this->m_Color[ 0 ] = r;
  this->m_Color[ 1 ] = g;
  this->m_Color[ 2 ] = b;
  this->m_Color[ 3 ] = a;
}

// -------------------------------------------------------------------------
void PUJ_CGraf::AmbientLight::
load( const unsigned long long& id )
{
  glLightfv( id, GL_AMBIENT, this->m_Color );
}

// eof - AmbientLight.cxx
