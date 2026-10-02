# BoaXR Assignment

Computer Vision/AI R&D internship assignment. Two parts: measure 3D meshes with an oriented bounding box, and pack 20 items into a box.

## Project Structure

```
BoaXR/
├── input/                  given files
│   ├── CUBE.obj
│   ├── CYLINDER.obj
│   ├── TEAPOT.obj
│   └── Item List.json
├── output/
│   ├── Part1/              OBB screenshots
│   └── Part2/              packing figure and animation
├── script/
│   ├── part1_obb.py
│   └── part2_pack.py
├── requirements.txt
└── Assignment Details.pdf
```

## Setup

```
pip install -r requirements.txt
```

Python 3.10 to 3.12 is recommended (Open3D wheels).

## Part 1: Oriented Bounding Box

Loads each .obj, finds the minimum-volume oriented bounding box (OBB), prints its size and volume, and draws the box in red around the mesh.

```
python script/part1_obb.py input/CUBE.obj input/CYLINDER.obj input/TEAPOT.obj
```

How it works:

1. `trimesh.load(force="mesh")` merges all parts into one mesh.
2. `bounding_box_oriented` builds the convex hull and keeps the rotation with the smallest box volume.
3. Sides are sorted as L >= W >= H. Volume = L x W x H.
4. Open3D draws the 12 box edges over the mesh.

The box is always a box. The mesh itself is not changed, so a cylinder still looks like a cylinder with a box around it.

Results (fill from the script output):

| Object   | L x W x H | Volume |
| -------- | --------- | ------ |
| CUBE     |           |        |
| CYLINDER |           |        |
| TEAPOT   |           |        |

Screenshots: `output/Part1/`

## Part 2: 3D Packing

Packs the 20 items from `Item List.json` into a 100 x 100 x 100 master box.

```
python script/part2_pack.py "input/Item List.json"
```

How it works:

1. Sort items by volume, biggest first.
2. Candidate spots are the origin plus three corners (right, behind, top) of every placed item.
3. For each item, try all 6 axis rotations at every spot.
4. Reject a spot if the item leaves the box, overlaps another item, or is not fully supported from below (floor, or the whole base sits on other items).
5. Pick the spot that keeps the bounding box of all placed items smallest.
6. Check the final layout again, then animate it one item at a time.

Result:

- All 20 items placed.
- Items fill 16.8% of the master box (168,250 of 1,000,000).
- Used space is 60 x 65 x 50, so 86.3% fill inside it.

Output: `output/Part2/packing.gif` and `output/Part2/Packing_Fig.png`

## Limits

- Part 2 is greedy, not optimal. Optimal 3D packing is NP-hard.
- Rotations are allowed. To keep the given orientation, use `[tuple(it["dims"])]` instead of `permutations(it["dims"])` in `part2_pack.py`.
- The support rule is strict (100% of the base).
- The OBB of a curved shape is looser than the shape. This is expected.

## Videos

[Google Drive folder](https://drive.google.com/drive/folders/1ZQolr3OK-Wd-4AquheH36nCB2NmsoQvK)
