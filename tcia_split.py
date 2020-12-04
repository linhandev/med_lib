import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-o", "--output", type=str, required=True)
parser.add_argument("-l", "--line", type=int, default=150)
args = parser.parse_args()

file_name = os.path.basename(args.input)[:-5]
if not os.path.exists(os.path.join(args.output, file_name)):
    os.makedirs(os.path.join(args.output, file_name))
    print("makedirs")

with open(args.input) as f:
    lines = f.readlines()
header = []
for _ in range(6):
    header.append(lines.pop(0))

print("total lines: ", len(lines))
part = 0
while (part + 1) * args.line < len(lines):
    outpath = os.path.join(args.output, file_name, str(part) + ".tcia")
    with open(outpath, "w") as f:
        for h in header:
            print(h, end="", file=f)
        for idx in range(part * args.line, (part + 1) * args.line):
            print(lines[idx], end="", file=f)
    part += 1

outpath = os.path.join(args.output, file_name, str(part) + ".tcia")
with open(outpath, "w") as f:
    for h in header:
        print(h, end="", file=f)
    for idx in range(part * args.line, len(lines)):
        print(lines[idx], end="", file=f)
