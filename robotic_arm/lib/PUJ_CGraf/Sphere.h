// =========================================================================
// @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
// =========================================================================
#ifndef __PUJ_CGraf__Sphere__h__
#define __PUJ_CGraf__Sphere__h__

#include <PUJ_CGraf/ParametricObject.h>

namespace PUJ_CGraf
{
  /**
   */
  class Sphere
    : public ParametricObject
  {
  public:
    using Self = Sphere;
    using Superclass = ParametricObject;
    using TReal = Superclass::TReal;
    using TNatural = Superclass::TNatural;
    using VReal = Superclass::VReal;
    using VNatural = Superclass::VNatural;

  public:
    Sphere( );
    virtual ~Sphere( ) = default;

    void set_center( const TReal& x, const TReal& y, const TReal& z );
    void set_radius( const TReal& r );

    virtual void point( TReal* p, const TReal& u, const TReal& v ) const override;
    virtual void normal( TReal* n, const TReal& u, const TReal& v ) const override;

  protected:
    TReal m_Center[ 3 ] { 0 };
    TReal m_Radius { 1 };
  };
} // end namespace

#endif // __PUJ_CGraf__Sphere__h__

// eof - Sphere.h
