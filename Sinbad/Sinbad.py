## -------------------------------------------------------------------------
## @author Leonardo Florez-Valencia (florez-l@javeriana.edu.co)
## -------------------------------------------------------------------------
## pip install wheel ogre-python
## -------------------------------------------------------------------------

import os, sys, tempfile, vtk
import Ogre, Ogre.Bites, Ogre.Overlay, Ogre.RTShader

## -------------------------------------------------------------------------
'''
Main application class
'''
class Main( Ogre.Bites.ApplicationContext, Ogre.Bites.InputListener ):

  '''
  Attributes for this classq
  '''
  m_MainDir = ''
  m_SceneManager = None
  m_CamMan = None

  '''
  '''
  def __init__( self, main_dir ):
    Ogre.Bites.ApplicationContext.__init__( self, 'Sinbad!' )
    Ogre.Bites.InputListener.__init__( self )
    self.m_MainDir = main_dir
  # end def

  '''
  '''
  def keyPressed( self, evt ):
    if evt.keysym.sym == Ogre.Bites.SDLK_ESCAPE:
      self.getRoot( ).queueEndRendering( )
    # end if
    return True
  # end def

  '''
  '''
  def loadResources( self ):
    self.enableShaderCache( )
    cf = Ogre.ConfigFile( )
    cf.loadDirect( os.path.join( self.m_MainDir, 'resources.cfg' ) )
    res_mgr = Ogre.ResourceGroupManager.getSingleton( )
    for k in cf.getSettingsBySection( ):
      s = cf.getSettings( k )
      for t, f in s.items( ):
        res_mgr.addResourceLocation( f, t, k )
      # end for
    # end for
    return Ogre.Bites.ApplicationContext.loadResources( self )
  # end def

  '''
  '''
  def create_simple_plane( self ):
    man = self.m_SceneManager.createManualObject( 'plane' )

    man.begin( 'Plane', Ogre.RenderOperation.OT_TRIANGLE_LIST )

    man.position( -10, 0, 10 )
    man.normal( 0, 1, 0 )
    man.textureCoord( 0, 0 )

    man.position( -10, 0, -10 )
    man.normal( 0, 1, 0 )
    man.textureCoord( 0, 1 )

    man.position( 10, 0, -10 )
    man.normal( 0, 1, 0 )
    man.textureCoord( 1, 1 )

    man.position( 10, 0, 10 )
    man.normal( 0, 1, 0 )
    man.textureCoord( 1, 0 )

    man.quad( 0, 1, 2, 3 )

    man.end( )
    self.m_SceneManager.getRootSceneNode( ).attachObject( man )
  # end def

  '''
  '''
  def load_stl( self, fname ):
    tf = tempfile.NamedTemporaryFile( 'w' )
    stream = Ogre.ResourceGroupManager.getSingleton( ).openResource( fname )
    tf.write( stream.getAsString( ) )

    reader = vtk.vtkSTLReader( )
    reader.SetFileName( tf.name )

    normals = vtk.vtkPolyDataNormals( )
    normals.SetInputConnection( reader.GetOutputPort( ) )
    normals.AutoOrientNormalsOn( )
    normals.ComputePointNormalsOn( )
    normals.ConsistencyOn( )
    normals.Update( )
    pdata = normals.GetOutput( )

    tf.close( )

    man = self.m_SceneManager.createManualObject( fname )
    man.begin( 'Plane', Ogre.RenderOperation.OT_TRIANGLE_LIST )

    for i in range( pdata.GetNumberOfPoints( ) ):
      px, py, pz = pdata.GetPoint( i )
      nx, ny, nz = pdata.GetPointData( ).GetNormals( ).GetTuple3( i )
      man.position( px, py, pz )
      man.normal( nx, ny, nz )
      # TODO: man.textureCoord( 0, 0 )
    # end for

    idx = vtk.vtkIdList( )
    for i in range( pdata.GetPolys( ).GetNumberOfCells( ) ):
      pdata.GetPolys( ).GetCellAtId( i, idx )
      man.triangle( idx.GetId( 0 ), idx.GetId( 1 ), idx.GetId( 2 ) )
    # end for

    man.end( )
    self.m_SceneManager.getRootSceneNode( ).attachObject( man )
  # end def

  '''
  '''
  def setup( self ):
    Ogre.Bites.ApplicationContext.setup( self )
    self.addInputListener( self )

    root = self.getRoot( )
    self.m_SceneManager = root.createSceneManager( )
    root_node = self.m_SceneManager.getRootSceneNode( )

    shadergen = Ogre.RTShader.ShaderGenerator.getSingleton( )
    shadergen.addSceneManager( self.m_SceneManager )

    self.m_SceneManager.addRenderQueueListener( self.getOverlaySystem( ) )

    self.m_SceneManager.setAmbientLight( ( 0.1, 0.1, 0.1 ) )

    light = self.m_SceneManager.createLight( 'MainLight' )
    lightnode = root_node.createChildSceneNode( )
    lightnode.setPosition( 0, 10, 15 )
    lightnode.attachObject( light )

    cam = self.m_SceneManager.createCamera( 'MainCamera' )
    cam.setNearClipDistance( 0.5 )
    cam.setAutoAspectRatio( True )
    camnode = root_node.createChildSceneNode( )
    camnode.attachObject( cam )

    self.m_CamMan = Ogre.Bites.CameraMan( camnode )
    self.m_CamMan.setStyle( Ogre.Bites.CS_ORBIT )
    self.m_CamMan.setYawPitchDist( 0, 0.3, 15 )
    self.addInputListener( self.m_CamMan )

    vp = self.getRenderWindow( ).addViewport( cam )
    vp.setBackgroundColour( ( 0.3, 0.3, 0.3 ) )

    ent = self.m_SceneManager.createEntity( 'Sinbad.mesh' )
    node = root_node.createChildSceneNode( )
    node.attachObject( ent )
  # end def

  '''
  '''
  def shutdown( self ):
    Ogre.Bites.ApplicationContext.shutdown( self )
  # end def

  '''
  '''
  def go( self ):
    self.initApp( )
    self.getRoot( ).startRendering( )
    self.closeApp( )
  # end def

# end class

## -------------------------------------------------------------------------
if __name__ == '__main__':
  app = Main( os.path.split( os.path.abspath( sys.argv[ 0 ] ) )[ 0 ] )
  app.go( )
# end if

## eof - Sinbad.py
