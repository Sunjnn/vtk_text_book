import vtk


def create_axes_actor(length=2.0):
    """创建坐标轴，方便观察变换效果"""
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(length, length, length)
    axes.AxisLabelsOn()
    return axes


def main():
    colors = vtk.vtkNamedColors()

    # === 创建一个立方体方便看旋转 ===
    cube_source = vtk.vtkCubeSource()
    cube_source.SetXLength(1)
    cube_source.SetYLength(0.5)
    cube_source.SetZLength(0.2)

    mapper1 = vtk.vtkPolyDataMapper()
    mapper1.SetInputConnection(cube_source.GetOutputPort())
    mapper2 = vtk.vtkPolyDataMapper()
    mapper2.SetInputConnection(cube_source.GetOutputPort())

    actor1 = vtk.vtkActor()
    actor1.SetMapper(mapper1)
    actor1.GetProperty().SetColor(colors.GetColor3d("Tomato"))

    actor2 = vtk.vtkActor()
    actor2.SetMapper(mapper2)
    actor2.GetProperty().SetColor(colors.GetColor3d("Banana"))

    # === (a) PreMultiply(默认) 模式 ===
    transform1 = vtk.vtkTransform()
    # 默认是 PreMultiply 模式
    transform1.Scale(1, 2, 1)
    transform1.RotateZ(45)
    transform1.Translate(1, 0, 0)
    actor1.SetUserTransform(transform1)

    # === (b) PostMultiplyOn 模式 ===
    transform2 = vtk.vtkTransform()
    transform2.PostMultiply()
    transform2.Scale(1, 2, 1)
    transform2.RotateZ(45)
    transform2.Translate(1, 0, 0)
    actor2.SetUserTransform(transform2)

    # === 场景 ===
    ren = vtk.vtkRenderer()
    ren.SetBackground(colors.GetColor3d("SlateGray"))

    # 添加坐标轴
    axes1 = create_axes_actor(2.5)

    ren.AddActor(actor1)
    ren.AddActor(actor2)
    ren.AddActor(axes1)

    # 光源
    light = vtk.vtkLight()
    light.SetPosition(5, 5, 5)
    light.SetFocalPoint(0, 0, 0)
    ren.AddLight(light)

    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(800, 800)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)

    ren_win.Render()
    iren.Initialize()
    iren.Start()


if __name__ == "__main__":
    main()
