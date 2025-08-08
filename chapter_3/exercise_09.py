import vtk


def main():
    colors = vtk.vtkNamedColors()

    # 创建立方体体数据源
    cube = vtk.vtkCubeSource()

    # 映射器
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(cube.GetOutputPort())

    # Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    print(f"cube position: {actor.GetPosition()}")

    actor.RotateX(20)
    actor.RotateY(30)
    actor.RotateZ(40)
    orientation = actor.GetOrientation()
    print(f"cube orientation: {orientation}")

    cube1 = vtk.vtkCubeSource()
    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputConnection(cube1.GetOutputPort())
    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    actor1.SetPosition(0, 0, 2)
    actor1.SetOrientation(orientation[0], orientation[1], orientation[2])

    # 渲染器
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.AddActor(actor1)
    ren.SetBackground(colors.GetColor3d("Black"))

    # 渲染窗口和交互
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(400, 400)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)
    iren.Initialize()

    ren_win.Render()
    iren.Start()


if __name__ == "__main__":
    main()
