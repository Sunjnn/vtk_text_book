import vtk

# === 1. 定义八面体的顶点 ===
# 一个规则八面体可以看作是两个四棱锥底对底拼接
# 顶点坐标（边长为 sqrt(2)）
points = vtk.vtkPoints()
points.InsertNextPoint( 1, 0, 0)  # 0
points.InsertNextPoint(-1, 0, 0)  # 1
points.InsertNextPoint( 0, 1, 0)  # 2
points.InsertNextPoint( 0,-1, 0)  # 3
points.InsertNextPoint( 0, 0, 1)  # 4 上顶点
points.InsertNextPoint( 0, 0,-1)  # 5 下顶点

# === 2. 定义八个三角形面 ===
# 每个三角形用 vtkTriangle 表示
faces = vtk.vtkCellArray()

def add_triangle(a, b, c):
    tri = vtk.vtkTriangle()
    tri.GetPointIds().SetId(0, a)
    tri.GetPointIds().SetId(1, b)
    tri.GetPointIds().SetId(2, c)
    faces.InsertNextCell(tri)

# 上半部分四个三角形
add_triangle(0, 2, 4)
add_triangle(2, 1, 4)
add_triangle(1, 3, 4)
add_triangle(3, 0, 4)

# 下半部分四个三角形
add_triangle(2, 0, 5)
add_triangle(1, 2, 5)
add_triangle(3, 1, 5)
add_triangle(0, 3, 5)

# === 3. 创建 PolyData ===
octahedron = vtk.vtkPolyData()
octahedron.SetPoints(points)
octahedron.SetPolys(faces)

# === 4. 映射器 ===
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputData(octahedron)

# === 5. Actor ===
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.8, 0.3) # 金黄色
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(0.0, 0.0, 0.0) # 黑色边线
actor.GetProperty().SetLineWidth(1.5)

# === 6. Renderer / RenderWindow / Interactor ===
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4) # 背景蓝
renderer.AddActor(actor)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(800, 600)
renWin.AddRenderer(renderer)
renWin.SetWindowName("Polygonal Octahedron")

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(renWin)

# === 7. 绘制 ===
renWin.Render()
interactor.Start()
