import vtk
import time


def main():
    colors = vtk.vtkNamedColors()

    # 创建球体数据源
    sphere = vtk.vtkSphereSource()
    sphere.SetPhiResolution(30)
    sphere.SetThetaResolution(30)

    # 映射器
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(sphere.GetOutputPort())

    # Actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # 设置材质属性
    prop = actor.GetProperty()
    prop.SetColor(1.0, 1.0, 1.0)  # 初始白色
    prop.SetAmbient(0.5)  # 环境光强度
    prop.SetDiffuse(0.5)  # 漫反射强度
    prop.SetSpecular(0.3)  # 高光强度（可调）
    prop.SetSpecularPower(20)  # 高光指数

    # 渲染器
    ren = vtk.vtkRenderer()
    ren.AddActor(actor)
    ren.SetBackground(colors.GetColor3d("Black"))

    # 渲染窗口和交互
    ren_win = vtk.vtkRenderWindow()
    ren_win.AddRenderer(ren)
    ren_win.SetSize(400, 400)

    ren_win.Render()

    input("Press any key to continue...")

    # 循环变换颜色
    # 漫反射颜色: 红 (1,0,0) -> 蓝 (0,0,1)
    # 环境光颜色: 蓝 (0,0,1) -> 绿 (0,1,0)
    steps = 100
    for i in range(steps + 1):
        t = i / steps  # 0 ~ 1 之间

        # 线性插值漫反射颜色
        diffuse_r = 1.0 - t  # 红分量从1降到0
        diffuse_g = 0.0  # 始终为0
        diffuse_b = t  # 蓝分量从0升到1

        # 线性插值环境光颜色
        amb_r = 0.0
        amb_g = t  # 绿从0升到1
        amb_b = 1.0 - t  # 蓝从1降到0

        prop.SetDiffuseColor(diffuse_r, diffuse_g, diffuse_b)
        prop.SetAmbientColor(amb_r, amb_g, amb_b)

        print(f"render step: {i}")
        ren_win.Render()
        time.sleep(0.02)  # 控制刷新速度


if __name__ == "__main__":
    main()
