"""
Convert Microsoft VoTTT exported voc to nvidia DIGIT kitti format
"""

import argparse
import os
import sys
import csv
import xml.etree.ElementTree as ET
import shutil

def parse_args():
    parser = argparse.ArgumentParser(description="Convert voc to kitti.")
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    required.add_argument('--from', dest='from_path',
                          required=True,
                          help=f'Path to dataset you wish to convert.', type=str)
    required.add_argument('--to',
                          dest='to_path', required=True,
                          help="Path to output directory for converted dataset.", type=str)

    args = parser.parse_args()
    return args

def convert(*, from_path, to_path):
    print(f"start convert from : {from_path} to {to_path}")

    #create labels / images dir if not exists
    if not (os.path.exists(f"{to_path}/labels")):
        os.mkdir(f"{to_path}/labels")
    if not (os.path.exists(f"{to_path}/images")):
        os.mkdir(f"{to_path}/images")

    annotations_path = f"{from_path}/Annotations"
    for f in os.listdir(annotations_path):
        f_name, f_ext = os.path.splitext(f)
        tree = ET.parse(os.path.join(annotations_path, f))
        root = tree.getroot()
        image_file_path = root.findtext("path")

        print(image_file_path)

        #copy image file
        img_name  = os.path.basename(image_file_path)
        shutil.copyfile(image_file_path, f"{to_path}/images/{img_name}")

        #create label
        output_label_file_path = f"{to_path}/labels/{f_name}.txt"
        print(f"output: {output_label_file_path}")
        output_file = open(output_label_file_path, 'w')

        for a in root.iter("object"):
            label = a.findtext("name")
            xmin = a.findtext("bndbox/xmin")
            ymin = a.findtext("bndbox/ymin")
            xmax = a.findtext("bndbox/xmax")
            ymax = a.findtext("bndbox/ymax")
            line = f"{label} 0 0 0 {xmin} {ymin} {xmax} {ymax} 0 0 0 0 0 0 0 0\n"
            print(line)
            output_file.writelines(line)

        output_file.close()


if __name__ == '__main__':
    args = parse_args()
    sys.exit(convert(from_path=args.from_path, to_path=args.to_path))
