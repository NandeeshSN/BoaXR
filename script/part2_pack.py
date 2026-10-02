import json, sys
from itertools import permutations
import numpy as np

BOX = 100

def overlap(p, d, q, e):
    return all(p[i] < q[i] + e[i] and q[i] < p[i] + d[i] for i in range(3))

def supported(p, d, placed):
    
    if p[2] == 0:
        return True
    got = 0
    for q, e, _ in placed:
        if q[2] + e[2] == p[2]:
            ox = min(p[0] + d[0], q[0] + e[0]) - max(p[0], q[0])
            oy = min(p[1] + d[1], q[1] + e[1]) - max(p[1], q[1])
            if ox > 0 and oy > 0:
                got += ox * oy
    return got >= d[0] * d[1]

def pack(items):
    items = sorted(items, key=lambda i: -np.prod(i["dims"]))  
    placed, pts, skipped = [], {(0, 0, 0)}, []
    for it in items:
        best = None
        for d in set(permutations(it["dims"])):  
            for p in pts:
                if any(p[i] + d[i] > BOX for i in range(3)):
                    continue
                if any(overlap(p, d, q, e) for q, e, _ in placed):
                    continue
                if not supported(p, d, placed):
                    continue
                
                ex = [max([p[i] + d[i]] + [q[i] + e[i] for q, e, _ in placed]) for i in range(3)]
                score = (ex[0] * ex[1] * ex[2], p[2], p[1], p[0])
                if best is None or score < best[0]:
                    best = (score, p, d)
        if best is None:
            skipped.append(it["id"]); continue
        _, p, d = best
        placed.append((p, d, it["id"]))
        pts |= {(p[0] + d[0], p[1], p[2]), (p[0], p[1] + d[1], p[2]), (p[0], p[1], p[2] + d[2])}
    return placed, skipped

def check(placed):
    for i, (p, d, _) in enumerate(placed):
        assert all(0 <= p[k] and p[k] + d[k] <= BOX for k in range(3))
        for q, e, _ in placed[:i]:
            assert not overlap(p, d, q, e)
        assert supported(p, d, placed[:i])

def animate(placed, out="output/Part2/packing.gif"):
    import matplotlib
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    def faces(p, d):
        x, y, z = p; a, b, c = d
        v = np.array([[x,y,z],[x+a,y,z],[x+a,y+b,z],[x,y+b,z],
                      [x,y,z+c],[x+a,y,z+c],[x+a,y+b,z+c],[x,y+b,z+c]])
        return [[v[i] for i in f] for f in
                [[0,1,2,3],[4,5,6,7],[0,1,5,4],[2,3,7,6],[1,2,6,5],[0,3,7,4]]]
    fig = plt.figure(figsize=(7, 7)); ax = fig.add_subplot(111, projection="3d")
    cmap = plt.get_cmap("tab20")
    def draw(n):
        ax.clear()
        ax.set_xlim(0, BOX); ax.set_ylim(0, BOX); ax.set_zlim(0, BOX)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(25, 35 + n * 2)
        ax.set_title(f"Packed {min(n, len(placed))}/{len(placed)}")
        for p, d, i in placed[:n]:  
            ax.add_collection3d(Poly3DCollection(faces(p, d), facecolors=cmap(i % 20),
                                                 edgecolors="k", alpha=0.85))
    ani = FuncAnimation(fig, draw, frames=len(placed) + 6, interval=700)
    ani.save(out, writer="pillow")
    if matplotlib.get_backend().lower() != "agg":
        plt.show()

if __name__ == "__main__":
    items = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "input/Item List.json"))
    placed, skipped = pack(items)
    check(placed)
    print("id  position       dims")
    for p, d, i in placed:
        print(f"{i:>2}  {str(p):<14} {d}")
    used = sum(int(np.prod(d)) for _, d, _ in placed)
    ex = [max(p[k] + d[k] for p, d, _ in placed) for k in range(3)]
    print(f"placed {len(placed)}/{len(items)}, skipped {skipped}")
    print(f"item volume {used}, fill of master box {used/BOX**3:.1%}, "
          f"used envelope {ex} fill {used/np.prod(ex):.1%}")
    animate(placed)
