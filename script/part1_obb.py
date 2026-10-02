import sys
import numpy as np
import trimesh

def obb_of(path):
    mesh = trimesh.load(path, force="mesh")           
    if mesh.is_empty:
        raise ValueError(f"{path}: no geometry")
    box = mesh.bounding_box_oriented                 
    L, W, H = sorted(box.primitive.extents, reverse=True)
    return mesh, box, (L, W, H), box.volume

def show(path):
    import open3d as o3d
    mesh, box, dims, vol = obb_of(path)
    print(f"{path}: L x W x H = {dims[0]:.3f} x {dims[1]:.3f} x {dims[2]:.3f}, volume = {vol:.3f}")
    m = o3d.geometry.TriangleMesh(o3d.utility.Vector3dVector(mesh.vertices),
                                  o3d.utility.Vector3iVector(mesh.faces))
    m.compute_vertex_normals(); m.paint_uniform_color([0.7, 0.7, 0.8])
    
    c = np.array(trimesh.bounds.corners(np.array([[-.5] * 3, [.5] * 3])))
    c = trimesh.transform_points(c * box.primitive.extents, box.primitive.transform)
    
    from itertools import combinations
    ext = sorted(box.primitive.extents)
    edges = [(i, j) for i, j in combinations(range(8), 2)
             if min(abs(np.linalg.norm(c[i] - c[j]) - e) for e in ext) < 1e-6 * max(ext)]
    ls = o3d.geometry.LineSet(o3d.utility.Vector3dVector(c), o3d.utility.Vector2iVector(edges))
    ls.paint_uniform_color([1, 0, 0])
    o3d.visualization.draw_geometries([m, ls], window_name=path) 

if __name__ == "__main__":
    files = sys.argv[1:] or ["input/CUBE.obj", "input/CYLINDER.obj", "input/TEAPOT.obj"]
    for f in files:
        try:
            show(f)
        except Exception as e:                        
            print(f"{f}: failed, {e}")
