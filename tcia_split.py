import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, required=True)
parser.add_argument("-o", "--output", type=str, required=True)
parser.add_argument("-l", "--line", type=int, default=100)
args = parser.parse_args()

if not os.path.exists(args.output):
    os.makedirs(args.output)

with open(args.input) as f:
    lines = f.readlines()
header = []
for _ in range(6):
    header.append(lines.pop(0))

file_name = os.path.basename(args.input)
print("total lines: ", len(lines))
part = 0
while (part + 1) * args.line < len(lines):
    outpath = os.path.join(args.output, file_name + "-" + str(part))
    with open(outpath, "w") as f:
        for h in header:
            print(h)
            print(h, end="", file=f)
        for idx in range(part * args.line, (part + 1) * args.line):
            print(lines[idx], end="", file=f)
    part += 1

outpath = os.path.join(args.output, file_name + "-" + str(part))
with open(outpath, "w") as f:
    for h in header:
        print(h)
        print(h, end="", file=f)
    for idx in range(part * args.line, len(lines)):
        print(lines[idx], end="", file=f)
