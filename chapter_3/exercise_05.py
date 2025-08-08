import vtk
import time


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

    ren_win.Render()

    input("Press any key to continue...")

    # 循环变换颜色
    # 漫反射颜色: 红 (1,0,0) -> 蓝 (0,0,1)
    # 环境光颜色: 蓝 (0,0,1) -> 绿 (0,1,0)
    steps = 1000
    for i in range(steps + 1):
        t = i / steps

        near = t
        far = camera.GetClippingRange()[1]

        print(f"render step: {i}, clipping range: {near}, {far}")
        camera.SetClippingRange(near, far)

        ren_win.Render()
        time.sleep(0.02)


if __name__ == "__main__":
    main()
