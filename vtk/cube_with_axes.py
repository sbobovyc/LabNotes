from __future__ import print_function
import vtk
# The colors module defines various useful colors.
from vtk.util.colors import tomato

class vtkTimerCallback():
   def __init__(self):
       self.timer_count = 0
 
   def execute(self,obj,event):
       print(self.timer_count)
       iren = obj
       ren.GetActiveCamera().Roll(5)
       iren.GetRenderWindow().Render()
       self.timer_count += 1

class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
 
    def __init__(self,parent=None):
        self.AddObserver("MiddleButtonPressEvent",self.middleButtonPressEvent)
        self.AddObserver("MiddleButtonReleaseEvent",self.middleButtonReleaseEvent)
 
    def middleButtonPressEvent(self,obj,event):
        print("Middle Button pressed")
	print(ren.GetActiveCamera().GetModelViewTransformMatrix())
        self.OnMiddleButtonDown()
        return
 
    def middleButtonReleaseEvent(self,obj,event):
        print("Middle Button released")
        self.OnMiddleButtonUp()
        return

# This creates a cube
cube = vtk.vtkCubeSource()
cube.SetXLength(25)
cube.SetYLength(3)
cube.SetZLength(40)
 
# The mapper is responsible for pushing the geometry into the graphics
# library. It may also do color mapping, if scalars or other
# attributes are defined.
cubeMapper = vtk.vtkPolyDataMapper()
cubeMapper.SetInputConnection(cube.GetOutputPort())
 
# The actor is a grouping mechanism: besides the geometry (mapper), it
# also has a property, transformation matrix, and/or texture map.
# Here we set its color and rotate it -22.5 degrees.
cubeActor = vtk.vtkActor()
cubeActor.SetMapper(cubeMapper)
cubeActor.GetProperty().SetColor(tomato)
#cubeActor.RotateX(30.0)
#cubeActor.RotateY(-45.0)

# Create the graphics structure. The renderer renders into the render
# window. The render window interactor captures mouse events and will
# perform appropriate camera or actor manipulation depending on the
# nature of the events.
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
#iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
iren.SetInteractorStyle(MyInteractorStyle())
iren.SetRenderWindow(renWin)


axes = vtk.vtkAxesActor()
widget = vtk.vtkOrientationMarkerWidget()
widget.SetOutlineColor( 0.9300, 0.5700, 0.1300 )
widget.SetOrientationMarker(axes)
widget.SetInteractor(iren)
widget.SetViewport( 0.0, 0.0, 0.4, 0.4 )
widget.SetEnabled(1)
widget.InteractiveOn()

# Add the actors to the renderer, set the background and size
ren.AddActor(cubeActor)
ren.SetBackground(0.1, 0.2, 0.4)
renWin.SetSize(800, 800)
 
# This allows the interactor to initalize itself. It has to be
# called before an event loop.
iren.Initialize()

cb = vtkTimerCallback()
iren.AddObserver('TimerEvent', cb.execute)
iren.CreateRepeatingTimer(100)
 
# We'll zoom in a little by accessing the camera and invoking a "Zoom"
# method on it.
ren.ResetCamera()
ren.GetActiveCamera().Zoom(0.5)
ren.GetActiveCamera().Elevation(45)
ren.GetActiveCamera().Roll(-15)
renWin.Render()
renWin.SetWindowName("Cube with axes")
 
# Start the event loop.
iren.Start()
