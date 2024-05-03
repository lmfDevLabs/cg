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

from KochanekBartelsSpline import KochanekBartelsSpline
import sys, vtk
from DijkstraOnVTKImage import *

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