## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================

import random, sys

'''
----------------------------------------------------------------------------
'''
def CreateFB( w, h ):
  I = [ 0 for i in range( w * h * 3 ) ]
  return ( I, w, h )
# end def

'''
----------------------------------------------------------------------------
'''
def ClearFB( B, c ):
  for i in range( 0, len( B[ 0 ] ), 3 ):
    B[ 0 ][ i ]     = c[ 0 ]
    B[ 0 ][ i + 1 ] = c[ 1 ]
    B[ 0 ][ i + 2 ] = c[ 2 ]
  # end for
# end def

'''
----------------------------------------------------------------------------
'''
def Pixel( B, p ):
  i = 3 * ( ( p[ 1 ] * B[ 1 ] ) + p[ 0 ] )
  return ( B[ 0 ][ i ], B[ 0 ][ i + 1 ], B[ 0 ][ i + 2 ] )
# end def

'''
----------------------------------------------------------------------------
'''
def DrawPixel( B, p, c ):
  i = 3 * ( ( p[ 1 ] * B[ 1 ] ) + p[ 0 ] )
  B[ 0 ][ i ]     = c[ 0 ]
  B[ 0 ][ i + 1 ] = c[ 1 ]
  B[ 0 ][ i + 2 ] = c[ 2 ]
# end def

'''
----------------------------------------------------------------------------
'''
def DrawLine( B, p0, p1, c ):
  x0 = p0[0]
  y0 = p0[1]
  x1 = p1[0]
  y1 = p1[1]

  dx = x1 - x0
  dy = y1 - y0
  D = 2 * dy - dx
  y = y0

  for x in range(x0,x1 +1):
    DrawPixel(B,(x,y),c)
    if D > 0:
      y += 1
      D -= 2 * dx
    D += 2 * dy
# end def

'''
----------------------------------------------------------------------------
'''
def DumpFB( B, fname ):
  out = "P3\n"
  out += str( B[ 1 ] ) + " " + str( B[ 2 ] ) + "\n255\n"
  for h in range( B[ 2 ] ):
    for w in range( B[ 1 ] ):
      p = Pixel( B, ( w, h ) )
      out += str( p[ 0 ] ) + " "
      out += str( p[ 1 ] ) + " "
      out += str( p[ 2 ] ) + " "
    # end for
    out += "\n"
  # end for
  outf = open( out_fname, "w" )
  outf.write( out )
  outf.close( )
# end def

'''
----------------------------------------------------------------------------
Usage:
python drawlines.py out.ppm w h x0 y0 x1 y1 r g b x0 y0 x1 y1 r g b ...
'''
   
if len( sys.argv ) < 11:
  print(
    "Usage: python "
    +
    sys.argv[ 0 ]
    +
    " out.ppm w h x0 y0 x1 y1 r g b x0 y0 x1 y1 r g b ..."
    )
  sys.exit( 1 )
# end if

# Get input parameters
out_fname = sys.argv[ 1 ]
width = int( sys.argv[ 2 ] )
height = int( sys.argv[ 3 ] )

# Create initial framebuffer
B = CreateFB( width, height )
ClearFB( B, ( 255, 255, 255 ) )

# Draw lines
for i in range( 4, len( sys.argv ), 7 ):
  x0 = int( sys.argv[ i ] )
  y0 = int( sys.argv[ i + 1 ] )
  x1 = int( sys.argv[ i + 2 ] )
  y1 = int( sys.argv[ i + 3 ] )
  r = int( sys.argv[ i + 4 ] )
  g = int( sys.argv[ i + 5 ] )
  b = int( sys.argv[ i + 6 ] )

  DrawLine( B, ( x0, y0 ), ( x1, y1 ), ( r, g, b ) )
  
# end for

# Save image
DumpFB( B, out_fname )

## eof - fill_boxes.py
