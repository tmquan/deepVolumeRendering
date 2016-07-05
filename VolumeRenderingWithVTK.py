#!/usr/bin/env python
# This file is a part of Dolfin project
__author__ 	= "Tran Minh Quan"
__license__ 	= "GPL"
__version__ 	= "0.0.1"
__date__	= "2016-07-06"
__email__ 	= "quantm@unist.ac.kr"

from vtk import *

# Construct the color functor and opacity (transparency) functor
reader 		= vtkTIFFReader()
mapper 		= vtkFixedPointVolumeRayCastMapper()
property 	= vtkVolumeProperty()
colorFunc 	= vtkColorTransferFunction()
opacityFunc	= vtkPiecewiseFunction()
volume 		= vtkVolume()


# Read the tif file to vtk reader
reader.SetFileName('foot.tif')
reader.Update()


# Set up the Mapper
mapper.SetInputConnection(reader.GetOutputPort())
mapper.SetBlendModeToMaximumIntensity()


# Set up the Property
colorFunc.AddRGBSegment(0.0,   0.0, 0.0, 0.0, 
			255.0, 1.0, 1.0, 1.0)
opacityWindow = 4096
opacityLevel  = 1024
opacityFunc.AddSegment(opacityLevel - 0.5*opacityWindow, 0.0,
      				   opacityLevel + 0.5*opacityWindow, 1.0 )
property.SetIndependentComponents(True)
property.SetColor(colorFunc)
property.SetScalarOpacity(opacityFunc)
property.SetInterpolationTypeToLinear()


# Set up the Volume 
volume.SetMapper(mapper)
volume.SetProperty(property)
# Set up the renderer
render 	= vtkRenderer()
render.SetBackground(0,0,0)
# Add volume
render.AddVolume(volume)


# Set up the windows
renWin	= vtkRenderWindow()
renWin.SetSize(512, 512)
renWin.AddRenderer(render)


# Set up the interactor
iren 	= vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

# Set up the camera
camera  = render.GetActiveCamera()
center 	= volume.GetCenter()
camera.SetFocalPoint(center[0], center[1], center[2])
camera.SetPosition(center[0], center[1]-512, center[2])
camera.SetViewUp(0, 0, -1)

# Start renderer
renWin.Render()
iren.Initialize()
iren.Start()
