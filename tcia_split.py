import os


tcia_path = "/home/lin/Desktop/4dlung.tcia"
splie_folder = "/home/lin/Desktop/4dlung"
part_count = 10


with open(tcia_path) as f:
    lines = f.readlines()
headers = lines[:6]
print(headers)

records_per_split = int((len(lines) - 6) / part_count) + 1

for file_ind in range(part_count):
    split_path = os.path.join(splie_folder, "{}.tcia".format(file_ind))
    with open(split_path, "w") as f:
        for header in headers:
            print(header, file=f, end="")
        for ind in range(records_per_split * file_ind, min(records_per_split * (file_ind + 1), len(lines) - 6)):
            print(ind)
            print(lines[ind + 6], file=f, end="")
