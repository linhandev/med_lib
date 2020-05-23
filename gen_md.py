md_file = "/home/lin/Desktop/out.md"
csv_file = "/home/lin/Desktop/data.csv"

in_file = open(csv_file)
lines = in_file.readlines()

of = open(md_file, "w")
# print(lines)
ismore = False
ind = 0
count = 0
direction = 0
for line in lines:
    fields = line.split(",")
    print(ind, fields)
    # print(fields[0] == "more")

    while len(fields) <= 4:
        fields.append("")

    if fields[0].startswith("#"):
        direction += 1
        continue

    if fields[1] == "数据集简称":
        continue

    if fields[0] == "more":
        break

    if fields[1] == "":
        continue

    # print(fields)
    count += 1
print("当前共收录 {} 个放向的 {} 个数据集".format(direction, count), file=of)

# input("pause")


for line in lines:
    fields = line.split(",")
    print(ind, fields)

    while len(fields) <= 15:
        fields.append("")

    ind += 1
    if fields[1] == "数据集简称":
        continue

    if fields[0].startswith("#"):
        print(fields[0], file=of)
        continue

    if fields[0] == "more":
        ismore = True
        continue

    if fields[1] == "":
        continue

    if ismore:
        print(fields[1], "\n", file=of)
        continue

    f = fields

    print("\n| 名称      | 标注内容 | 类型 | 模态 | 数量 | 标签格式 | 文件格式 |", file=of)
    print("| - | - | - | - | - | - | - |", file=of)

    if f[3].startswith("["):
        print("|{} {}".format(f[1], f[3]), end="", file=of)
    else:
        print("| [{}]({}) ".format(f[1], f[3]), end="", file=of)

    print("| {}  | {}  | {}   | {}  | {}  | {} |".format(f[6], f[7], f[5], f[8], f[9], f[10]), file=of)
    print(f[11], end="", file=of)
    if f[12] != "":
        print("  相关项目：", f[12], file=of)

    if f[13] != "":
        print("  介绍论文：", f[13], file=of)
    if f[14].startswith("["):
        print("\n", f[14], file=of)
    elif f[14] != "":
        print("\n[Aistudio下载]({})".format(f[14]), file=of)

    # input("pause")
    # print(fields)
