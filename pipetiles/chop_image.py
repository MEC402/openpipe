import cv2
import sys
import os
from os.path import isfile, isdir


# input_pano is the equirectangular panorama to be tiled.
# output_dir is the output directory where the tiles are going to be stored.
# levels is the number of resolution levels that are generated.
# tmp_dir is an optional argument and sets the temporal directory where the
#           intermediate files are stored.

tile_w = 512
tile_h = 512

def generate_dir_tree(output_dir, levels, faces):
    os.mkdir(output_dir)
    for level in range(1,levels+1):
        ldirname = output_dir + "/" + str(level)
        os.mkdir(ldirname)
        for face in faces:
            fdirname = ldirname + "/" + face
            os.mkdir(fdirname)
            h = pow(2,(level-1));
            for row in range(0,h):
                rdirname = fdirname + "/" + str(row)
                os.mkdir(rdirname)

def generate_tile(img, i, j, tile_h, tile_w, outfile):
    x = i * tile_w
    y = j * tile_h
    tile = img[y:y+tile_h, x:x+tile_w]
    cv2.imwrite(outfile, tile)

def generate_face_tiles(output_dir, levels, face, imgprefix):
    filename = imgprefix + "_" + face + ".png"
    print(filename)
    img = cv2.imread(filename)

    for level in reversed(range(1, levels+1)):
        h = pow(2,(level-1));
        for row in range(0,h):
            for col in range(0,h):
                print("\tLevel: [{l}]  Face: {f},  ({r}, {c})".format(l=level, f=face, r=row, c=col))
                outfile = output_dir + "/" + str(level) + "/" + face + "/" + str(row) + "/" + str(col) + ".png"
                generate_tile(img, row, col, tile_h, tile_w, outfile)
        img = cv2.resize(img, None, fx=0.5, fy=0.5)



if len(sys.argv) < 3:
  print("Incorrect number of arguments!")
  print("Usage: python generate_tiles.py input_pano output_dir levels [tmp_dir]")
  exit("Terminated")


output_dir = sys.argv[2]
levels = int(sys.argv[3])

tmp = '.'
if len(sys.argv) == 5:
    tmp = sys.argv[4]

#Cube faces generation
cmd ="/home/STEVENCUTCHIN/bin/panorama -i {input_pano} -o {tmp_dir}/cube_face -r 4096".format(input_pano=sys.argv[1], tmp_dir=tmp)
os.system(cmd)


faces = {"0", "1", "2", "3", "4", "5"}#,"d","b","f","l","r"
imgprefix = "{}/cube_face".format(tmp)

generate_dir_tree(output_dir, levels, faces)
for face in faces:
    generate_face_tiles(output_dir, levels, face, imgprefix)
print("Done!")
