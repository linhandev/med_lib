import os

import numpy as np

with open("./names.txt") as f:
    data = f.readlines()
levels = {}
data = [d.split("\t") for d in data]
print(data[0])
for d in data:
    if len(d) != 2:
        continue
    d[1] = d[1].rstrip("\n")
    if d[1] == "空" or len(d[1]) == 0:
        continue
    levels[d[0]] = int(d[1])

for fname in os.listdir("diameter"):
    # print('"' + fname[:-4] + '"', end=",")
    print(fname, end="\t")

    with open("./diameter/{}".format(fname)) as f:
        data = f.readlines()

    mins = []
    for l in data:
        l = l.split(",")
        l = l[1:]
        t = []
        for data in l:
            if len(data) > 5 and float(data) > 10:
                t.append(float(data))
        if len(t) > 0:
            mins.append(np.min(t))

    mins = [d for d in mins if d > 11]
    res = np.mean(mins) + np.std(mins)
    print((res - 15) / 55, end="\t")
    try:
        print(levels[fname[:-11]])
    except:
        print()
print("\n")
