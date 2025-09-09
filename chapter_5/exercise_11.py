import vtk
import math

# 参数设置
R_outer = 2.0      # 外半径
R_inner = 1.0      # 内半径
Z_min   = -2.0     # 圆柱下端
Z_max   =  2.0     # 圆柱上端
nr      = 10       # 径向点数
nt      = 50       # 周向点数
nz      = 20       # 纵向点数（高度方向）

# Structured Grid 创建
points = vtk.vtkPoints()


# 按 (r, theta, z) 顺序生成点
for k in range(nz):
    z = Z_min + (Z_max - Z_min) * k / (nz - 1)
    for j in range(nt):
        theta = 2.0 * math.pi * j / (nt - 1)
        for i in range(nr):
            r = R_inner + (R_outer - R_inner) * i / (nr - 1)
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            points.InsertNextPoint(x, y, z)

# 创建 StructuredGrid 对象
sg = vtk.vtkStructuredGrid()
sg.SetDimensions(nr, nt, nz)
sg.SetPoints(points)

# 为了显示表面，我们可以用 DataSetSurfaceFilter
surface_filter = vtk.vtkDataSetSurfaceFilter()
surface_filter.SetInputData(sg)
surface_filter.Update()

# 映射器
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(surface_filter.GetOutputPort())

# Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.8, 0.3)  # 金黄色

# Renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)  # 背景蓝色
renderer.AddActor(actor)

# 渲染窗口
render_window = vtk.vtkRenderWindow()
render_window.SetWindowName("Hollow Cylinder Structured Grid")
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)

# 交互器
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
