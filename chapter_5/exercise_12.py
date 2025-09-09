import vtk
import math

# 参数
R_outer = 2.0
R_inner = 1.0
height  = 4.0
nt = 50  # 周向分段
nz = 20  # 高度方向分段

# 创建点
points = vtk.vtkPoints()

def insert_ring_points(r, z):
    for j in range(nt):
        theta = 2.0 * math.pi * j / nt
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.InsertNextPoint(x, y, z)

# 两层（外、内）重复 nz+1 层高度
for k in range(nz+1):
    z = -height/2.0 + (height * k) / nz
    insert_ring_points(R_outer, z)  # 外圈
    insert_ring_points(R_inner, z)  # 内圈

# 创建 UnstructuredGrid
ugrid = vtk.vtkUnstructuredGrid()
ugrid.SetPoints(points)

# 帮助定位点 index
def outer_index(j, k):
    """外圈点索引"""
    return k*(2*nt) + j

def inner_index(j, k):
    """内圈点索引"""
    return k*(2*nt) + nt + j

# 添加侧面（外壁）
for k in range(nz):
    for j in range(nt):
        jp = (j+1) % nt
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, outer_index(j, k))
        quad.GetPointIds().SetId(1, outer_index(jp, k))
        quad.GetPointIds().SetId(2, outer_index(jp, k+1))
        quad.GetPointIds().SetId(3, outer_index(j, k+1))
        ugrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

# 添加侧面（内壁，注意法线方向相反）
for k in range(nz):
    for j in range(nt):
        jp = (j+1) % nt
        quad = vtk.vtkQuad()
        quad.GetPointIds().SetId(0, inner_index(jp, k))
        quad.GetPointIds().SetId(1, inner_index(j, k))
        quad.GetPointIds().SetId(2, inner_index(j, k+1))
        quad.GetPointIds().SetId(3, inner_index(jp, k+1))
        ugrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

# 可选：封顶和封底（两圈间连成 Quad）
# 顶面
k_top = nz
for j in range(nt):
    jp = (j+1) % nt
    quad = vtk.vtkQuad()
    quad.GetPointIds().SetId(0, outer_index(j, k_top))
    quad.GetPointIds().SetId(1, inner_index(j, k_top))
    quad.GetPointIds().SetId(2, inner_index(jp, k_top))
    quad.GetPointIds().SetId(3, outer_index(jp, k_top))
    ugrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

# 底面
k_bot = 0
for j in range(nt):
    jp = (j+1) % nt
    quad = vtk.vtkQuad()
    quad.GetPointIds().SetId(0, inner_index(j, k_bot))
    quad.GetPointIds().SetId(1, outer_index(j, k_bot))
    quad.GetPointIds().SetId(2, outer_index(jp, k_bot))
    quad.GetPointIds().SetId(3, inner_index(jp, k_bot))
    ugrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

# 映射器
mapper = vtk.vtkDataSetMapper()
mapper.SetInputData(ugrid)

# Actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.8, 0.3)  # 金黄色
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0)

# Renderer
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddActor(actor)

# 渲染窗口
renwin = vtk.vtkRenderWindow()
renwin.SetWindowName("Hollow Cylinder - UnstructuredGrid")
renwin.SetSize(800, 600)
renwin.AddRenderer(renderer)

# 交互器
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renwin)

renwin.Render()
iren.Start()
