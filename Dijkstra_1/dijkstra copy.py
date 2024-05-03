# Manual de Uso del Código de Dijkstra y Spline en Imágenes VTK
# Por Diego Alejandro Uribe y Carlos Alberto Talero Jácome

# 1. Descripción general
# Este código permite al usuario seleccionar dos puntos (semillas) en una imagen y calcular un camino entre estos puntos utilizando el algoritmo de Dijkstra. Posteriormente, este camino se suaviza utilizando la spline de Kochanek-Bartels.
# 2. Requisitos previos
# Python 3.x
# Bibliotecas: vtk
# Imagen en formato PNG para probar el código
# 3. Cómo ejecutar el código
# Abra una terminal o línea de comandos.
# Navegue al directorio que contiene el código y la imagen.
# Ejecute el código con el comando:
# Copy code
# python nombre_del_archivo.py imagen_de_prueba.png
# Seleccione dos puntos en la imagen que se muestra.
# Observará dos caminos: uno original (amarillo) y uno suavizado (cyan).
# 4. Explicación del código
# Lectura de la imagen: La imagen se carga en el programa utilizando vtk.vtkPNGReader().
# Selección de semillas: Se utiliza vtk.vtkSeedWidget() para permitir al usuario seleccionar dos puntos en la imagen.
# Algoritmo de Dijkstra: Se utiliza para calcular el camino más corto entre los dos puntos seleccionados en la imagen.
# Suavizado del camino: Se utiliza la spline de Kochanek-Bartels para suavizar el camino obtenido del algoritmo de Dijkstra.
# Visualización: Se utiliza VTK para visualizar tanto el camino original como el suavizado en la imagen.
# 5. Resolución de problemas comunes
# El camino no es visible: Asegúrese de que los dos puntos seleccionados no estén demasiado cerca uno del otro o en una región de la imagen con poco contraste.
# El camino suavizado no se muestra: Ajuste el valor z_offset para separar visualmente el camino original del suavizado.
# El camino toma una forma extraña: Verifique la imagen y los puntos seleccionados. Considere ajustar la función de costo o usar otra técnica de suavizado.


import sys, vtk
import heapq, math, vtk

def DijkstraOnVTKImage( image, s, e ):

    # Get image-as-graph properties
    W, H, D = image.GetDimensions( )
    T = [ [  None for j in range( H ) ] for i in range( W ) ]
    M = [ [ False for j in range( H ) ] for i in range( W ) ]
    si = [ 0, 0, 0 ]
    ei = [ 0, 0, 0 ]
    image.TransformPhysicalPointToContinuousIndex( [ s[ 0 ], s[ 1 ], 0 ], si )
    image.TransformPhysicalPointToContinuousIndex( [ e[ 0 ], e[ 1 ], 0 ], ei )

    # Compute spanning tree from s
    q = [ ( 0, [ int( si[ 0 ] ), int( si[ 1 ] ) ], None ) ]
    while len( q ) > 0:
        n = heapq.heappop( q )
        i = n[ 1 ]
        v = image.GetScalarComponentAsDouble( i[ 0 ], i[ 1 ], 0, 0 )
        if M[ i[ 0 ] ][ i[ 1 ] ] == False:
            M[ i[ 0 ] ][ i[ 1 ] ] = True
            T[ i[ 0 ] ][ i[ 1 ] ] = n[ 2 ]
            for d in range( 2 ):
                for o in range( -1, 2, 2 ):
                    ni = [ i[ 0 ], i[ 1 ] ]
                    ni[ d ] += o
                    if \
                        0 <= ni[ 0 ] and ni[ 0 ] < W \
                        and \
                        0 <= ni[ 1 ] and ni[ 1 ] < H:
                        w = image.GetScalarComponentAsDouble( ni[ 0 ], ni[ 1 ], 0, 0 )
                        w -= v
                        w = 1 - math.exp( -( w * w ) )
                        # w = math.exp( -( w * w ) )
                        heapq.heappush( q, ( n[ 0 ] + w, ni, i ) )
                    # end if
                # end for
            # end for
        # end if
    # end while

    # Backtracking
    points = vtk.vtkPoints( )
    i = [ int( ei[ 0 ] ), int( ei[ 1 ] ) ]
    while not T[ i[ 0 ] ][ i[ 1 ] ] is None:
        xyz = [ 0, 0, 0 ]
        image.TransformIndexToPhysicalPoint( [ i[ 0 ], i[ 1 ], 0 ], xyz )
        xyz[ 2 ] = 24
        points.InsertNextPoint( xyz )
        i = T[ i[ 0 ] ][ i[ 1 ] ]
    # end while

    line = vtk.vtkCellArray( )
    line.InsertNextCell( points.GetNumberOfPoints( ) )
    for i in range( points.GetNumberOfPoints( ) ):
        line.InsertCellPoint( i )
    # end for

    pdata = vtk.vtkPolyData( )
    pdata.SetPoints( points )
    pdata.SetLines( line )

    return pdata
# end def

## -------------------------------------------------------------------------
if __name__ == "__main__":
    import sys

    src = vtk.vtkImageNoiseSource( )
    src.SetWholeExtent( 0, 150, 0, 100, 0, 0 )
    src.SetMinimum( 0.0 )
    src.SetMaximum( 255.0 )
    src.Update( )

    path = DijkstraOnVTKImage( src.GetOutput( ), ( 10, 10 ), ( 123, 98 ) )
# end if
## eof - DijkstraOnVTKImage.py

class KochanekBartelsSpline:
    def __init__(self, control_points, T=0, C=0, B=0):
        self.control_points = control_points
        self.T = T
        self.C = C
        self.B = B

    def compute_tangent(self, pm1, p0, p1):
        d0 = ((1 - self.T) * (1 + self.C) * (1 + self.B)) / 2
        d1 = ((1 - self.T) * (1 - self.C) * (1 - self.B)) / 2
        return [d0 * (p1[i] - p0[i]) + d1 * (p0[i] - pm1[i]) for i in range(len(p0))]

    def interpolate(self, p0, p1, m0, m1, t):
        h00 = 2 * t**3 - 3 * t**2 + 1
        h10 = t**3 - 2 * t**2 + t
        h01 = -2 * t**3 + 3 * t**2
        h11 = t**3 - t**2
        return [h00 * p0[i] + h10 * m0[i] + h01 * p1[i] + h11 * m1[i] for i in range(len(p0))]

    def compute_curve(self, num_points=10):
        curve = []
        for i in range(len(self.control_points) - 1):
            p0 = self.control_points[i]
            p1 = self.control_points[i + 1]
            if i == 0:
                pm1 = p0
            else:
                pm1 = self.control_points[i - 1]
            if i + 2 >= len(self.control_points):
                p2 = p1
            else:
                p2 = self.control_points[i + 2]

            m0 = self.compute_tangent(pm1, p0, p1)
            m1 = self.compute_tangent(p0, p1, p2)

            for j in range(num_points):
                t = j / float(num_points - 1)
                curve.append(self.interpolate(p0, p1, m0, m1, t))
        return curve



image = vtk.vtkPNGReader()
image.SetFileName(sys.argv[1])

viewer = vtk.vtkImageViewer2()
viewer.SetInputConnection(image.GetOutputPort())
viewer.SetColorWindow(256)
viewer.SetColorLevel(128)
viewer.GetRenderWindow().SetSize(512, 512)
viewer.GetRenderer().SetBackground(1, 0, 0)
viewer.GetRenderWindow().SetWindowName('Dijkstra')

# Create the RenderWindowInteractor.
iren = vtk.vtkRenderWindowInteractor()
viewer.SetupInteractor(iren)

hrep = vtk.vtkPointHandleRepresentation2D()
hrep.GetProperty().SetColor(0, 1, 0)

wrep = vtk.vtkSeedRepresentation()
wrep.SetHandleRepresentation(hrep)

widget = vtk.vtkSeedWidget()
widget.SetInteractor(iren)
widget.SetRepresentation(wrep)

widget.On()
viewer.Render()
iren.Initialize()
iren.Start()

if wrep.GetNumberOfSeeds() > 1:
    s = [0, 0, 0]
    e = [0, 0, 0]
    
    wrep.GetSeedWorldPosition(0, s)
    wrep.GetSeedWorldPosition(1, e)
    print(s,e)
    
    dmap = vtk.vtkImageEuclideanDistance()
    dmap.SetInputConnection(image.GetOutputPort())
    dmap.Update()

    path = DijkstraOnVTKImage(dmap.GetOutput(), s, e)
    
    # Compute smoothed path using Kochanek–Bartels spline
    path_points = [path.GetPoint(i) for i in range(path.GetNumberOfPoints())]
    print(path_points)
    spline = KochanekBartelsSpline(path_points)
    smoothed_path = spline.compute_curve()
    print(smoothed_path)

    # Convert smoothed_path to vtkPolyData for visualization
    smoothed_path_polydata = vtk.vtkPolyData()
    points = vtk.vtkPoints()
    # for point in smoothed_path:
    #     points.InsertNextPoint(point)
    # smoothed_path_polydata.SetPoints(points)
    z_offset = 5.0  # Adjust this value as needed
    for point in smoothed_path:
        points.InsertNextPoint(point[0], point[1], point[2] + z_offset)
    smoothed_path_polydata.SetPoints(points)

    # Visualize the smoothed path alongside the original path using VTK
    smoothed_path_mapper = vtk.vtkPolyDataMapper()
    smoothed_path_mapper.SetInputData(smoothed_path_polydata)
    smoothed_path_actor = vtk.vtkActor()
    smoothed_path_actor.SetMapper(smoothed_path_mapper)
    smoothed_path_actor.GetProperty().SetColor(0, 1, 1)  # Setting the color to cyan for differentiation

    path_mapper = vtk.vtkPolyDataMapper()
    path_mapper.SetInputData(path)
    path_actor = vtk.vtkActor()
    path_actor.SetMapper(path_mapper)
    path_actor.GetProperty().SetColor(1, 1, 0)

    viewer = vtk.vtkImageViewer2()
    viewer.SetInputConnection(dmap.GetOutputPort())
    viewer.SetColorWindow(256)
    viewer.SetColorLevel(128)
    viewer.GetRenderWindow().SetSize(800, 800)
    viewer.GetRenderer().SetBackground(1, 0, 0)
    viewer.GetRenderWindow().SetWindowName('Dijkstra')

    # Create the RenderWindowInteractor.
    iren = vtk.vtkRenderWindowInteractor()
    viewer.SetupInteractor(iren)
    viewer.GetRenderer().AddActor(path_actor)
    viewer.GetRenderer().AddActor(smoothed_path_actor)

    viewer.Render()
    iren.Initialize()
    iren.Start()