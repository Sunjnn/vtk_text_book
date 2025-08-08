import vtk


def main():
    colors = vtk.vtkNamedColors()

    # 创建球体数据源
    sphere = vtk.vtkSphereSource()
    sphere.SetPhiResolution(30)
    sphere.SetThetaResolution(30)
    print(f"radius of sphere: {sphere.GetRadius()}")

    # 映射器
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())

    # Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    print(f"sphere position: {actor.GetPosition()}")

    # 设置材质属性
    prop = actor.GetProperty()
    prop.SetColor(1.0, 1.0, 1.0)  # 初始白色
    prop.SetAmbient(0.5)  # 环境光强度
    prop.SetDiffuse(0.5)  # 漫反射强度
    prop.SetSpecular(0.3)  # 高光强度（可调）
    prop.SetSpecularPower(20)  # 高光指数

    light = vtk.vtkLight()
    light.SetPosition(1, 1, 1)
    light.SetFocalPoint(0, 0, 0)

    # 渲染器
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(colors.GetColor3d("Black"))
    ren.AddLight(light)

    camera = ren.GetActiveCamera()
    camera.SetPosition(0, 0, 2)
    print(f"default clipping range: {camera.GetClippingRange()}")

    # 渲染窗口和交互
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(400, 400)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(ren_win)
    iren.Initialize()

    coordinate = [0, 0, 3, 1]
    point = vtk.vtkSphereSource()
    point.SetRadius(0.1)
    point_mapper = vtk.vtkPolyDataMapper()
    point_mapper.SetInputConnection(point.GetOutputPort())
    point_actor = vtk.vtkActor()
    point_actor.SetMapper(point_mapper)
    point_actor.SetPosition(
        coordinate[0] / coordinate[3],
        coordinate[1] / coordinate[3],
        coordinate[2] / coordinate[3],
    )
    ren.AddActor(point_actor)

    ren_win.Render()
    iren.Start()


if __name__ == "__main__":
    main()
