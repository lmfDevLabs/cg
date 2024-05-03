## =========================================================================
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## =========================================================================
## This example could be used as an introductory example of the complexity
## on computer graphics implementations.
## =========================================================================
## python3.10 fill_boxes.py out_py.ppm 2560 2048 50 50 50 50 50
## real    0m26.438s
## user    0m25.948s
## sys     0m0.489s
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
python fill_boxes.py out.ppm w h p2 p3 p4 ... pn
'''

if len( sys.argv ) < 4:
  print(
      "Usage: python "
      +
      sys.argv[ 0 ]
      +
      "out.ppm w h p2 p3 p4 ... pn"
      )
  sys.exit( 1 )
# end if

# Get input parameters
out_fname = sys.argv[ 1 ]
boxes = [ ( int( sys.argv[ 2 ] ), int( sys.argv[ 3 ] ), 100.0 ) ]
for i in range( 4, len( sys.argv ) ):
  p = float( sys.argv[ i ] ) / 100.0
  w = int( float( boxes[ -1 ][ 0 ] ) * p )
  h = int( float( boxes[ -1 ][ 1 ] ) * p )
  s = boxes[ -1 ][ 2 ] * p
  boxes += [ ( w, h, s ) ]
# end for

# Create initial framebuffer
B = CreateFB( boxes[ 0 ][ 0 ], boxes[ 0 ][ 1 ] )

# Prepare random filling
M = [ 127, 127, 127 ]
for b in boxes:
  W = b[ 0 ]
  H = b[ 1 ]
  S = b[ 2 ]

  for w in range( W ):
    for h in range( H ):
      r = int( random.gauss( M[ 0 ], S ) )
      g = int( random.gauss( M[ 1 ], S ) )
      b = int( random.gauss( M[ 2 ], S ) )
      if r < 0: r = 0
      if g < 0: g = 0
      if b < 0: b = 0
      if r > 255: r = 255
      if g > 255: g = 255
      if b > 255: b = 255
      DrawPixel( B, ( w, h ), ( r, g, b ) )
    # end for
  # end for
# end for

# Save image
DumpFB( B, out_fname )

## eof - fill_boxes.py
