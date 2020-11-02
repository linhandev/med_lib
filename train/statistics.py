import argparse
import os

import pydicom
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("--img_path", type=str, default="/home/lin/Desktop/data/aorta/not_labeled/dcm")
parser.add_argument("--out_fname", type=str, default="info")
args = parser.parse_args()

f = open("{}.csv".format(args.out_fname), "w")


def note(info):
    if info == "\n":
        print(file=f)
        return
    if isinstance(info, int):
        print(info, file=f, end=",")
        return

    if isinstance(info, list):
        for data in info:
            print(data, file=f, end=",")
        print(file=f)
        return
    if isinstance(info, str):
        print(info, file=f, end=",")
        return

    if isinstance(info, float):
        print(info, file=f, end=",")
        return

    if not info:
        print("None", file=f, end=",")
        return

    if info.keyword == "PatientAge":
        print(str(info.value).lstrip("0").rstrip("Y"), file=f, end=",")
        return

    if info.keyword == "PixelSpacing":
        # isinstance(info.value, pydicom.multival.MultiValue)
        print(info.value[0], file=f, end=",")
        print(info.value[1], file=f, end=",")
        return
    # print(info)
    # print(type(info.value))
    # print(info.keyword)
    # input("here\n")
    if isinstance(info.value, str) and info.value.endswith("kV"):
        print(info.value.rstrip("kV"), file=f, end=",")
        return

    if info.keyword == "WindowCenter" or info.keyword == "WindowWidth":
        if isinstance(info.value, pydicom.multival.MultiValue):
            print(info.value[0], file=f, end=",")
            return

    # print(info)
    # print(type(info))
    # input("here")

    print(info.value, file=f, end=",")


def score(data, split=0.2):
    if len(data) < 10:
        return -1, -1, -1, -1, -1

    mins = []
    # print("\n\n\n\n\n", data)
    for idx in range(len(data)):
        if len(data[idx]) == 1:
            continue
        mins.append(np.min(data[idx][1:]))
    # print(mins)
    abdomin = np.max(mins[: int(len(mins) * split)])
    chest = np.max(mins[int(len(mins) * split) :])
    if abdomin > 30:
        abdomin += 20
    res = max(abdomin, chest)
    if 40 < res < 50:
        cat1 = 1
    elif res > 50:
        cat1 = 2
    else:
        cat1 = 0
    if res > 39.5:
        cat2 = 1
    else:
        cat2 = 0
    if res > 50:
        cat3 = 1
    else:
        cat3 = 0
    # print(abdomin, chest, cat1, cat2, cat3)
    return abdomin, chest, cat1, cat2, cat3


def get_info(img_path):
    note(
        [
            "Patient Name",
            "Institution Name",
            "Patient ID",
            "Patient's Name",
            "Age",
            "Gender",
            "Voltage",
            "Current",
            "Manufacturer",
            "Pixel Spacing",
            "Pixel Spacing",
            "Slice Thickness",
            "Voxel Size",
            "Study Description",
            "Window Center",
            "Window Width",
            "Acquisition Date",
            "Pixel Padding Value",
            "Slice Count",
        ]
    )

    for img_folder, dir, files in os.walk(img_path):
        if len(dir) != 0 or len(files) < 50:
            continue
        print("++", img_folder)
        # print(img_folder)

        scans = os.listdir(img_folder)
        if len(scans) == 0:
            print(img_folder)
            continue
        scan = scans[0]
        file_path = os.path.join(img_folder, scan)
        try:
            hdr = pydicom.dcmread(os.path.join(img_path, file_path))
        except:
            print(img_folder)

        # print(
        #     "------------------------------------------------------------------------------------------------------------"
        # )
        # print(hdr)
        # # input("here")
        # print("\n\n\n\n\n")
        note(os.path.basename(img_folder).split("_")[0])
        try:
            note(hdr[0x0008, 0x0080])  # Institution Name
            note(hdr[0x0010, 0x0020])  # Patient ID
            note(hdr[0x0010, 0x0010])  # Patient's Name
            note(hdr[0x0010, 0x1010])  # Age
            note(hdr[0x0010, 0x0040])  # Gender

            # private header, may not be the same
            # Voltage
            if hdr["Manufacturer"].value == "NMS":
                note(hdr[0x0018, 0x0060])
            elif hdr["Manufacturer"].value == "Philips":
                note(hdr[0x0018, 0x0060])
            elif hdr["Manufacturer"].value == "SIEMENS":
                note(hdr[0x0018, 0x0060])
            elif hdr["Manufacturer"].value == "Hitachi Medical Corporation":
                note(hdr[0x0018, 0x0060])
            else:
                note(hdr[0x0053, 0x1066])  # Voltage
            note(hdr[0x0018, 0x1151])  # Current
            note(hdr["Manufacturer"])

            note(hdr[0x0028, 0x0030])  # Pixel Spacing
            note(hdr[0x0018, 0x0050])  # Slice Thickness
            note(hdr[0x0028, 0x0030].value[0] ** 2 * hdr[0x0018, 0x0050].value)

            # note(hdr[0x0008, 0x0070]) # Manufacturer

            note(hdr[0x0008, 0x1030])  # Study Description
            note(hdr[0x0028, 0x1050])  # Window Center
            note(hdr[0x0028, 0x1051])  # Window Width
            # print(hdr[0x0028, 0x1050])
            # print(hdr[0x0028, 0x1051])
            # input("here")
            note(hdr[0x0008, 0x0022])  # Acquisition Date

            if hdr["Manufacturer"].value == "NMS":
                note(None)
            elif hdr["Manufacturer"].value == "Philips":
                note(None)
            elif hdr["Manufacturer"].value == "SIEMENS":
                note(None)
            elif hdr["Manufacturer"].value == "Hitachi Medical Corporation":
                note(None)
            else:
                note(hdr[0x0028, 0x0120])  # Pixel Padding Value

            note(len(os.listdir(img_folder)) - 1)

            dataf = open(
                os.path.join(
                    "/home/lin/Desktop/data/aorta/not_labeled/diameters", os.path.basename(img_folder) + ".csv"
                ),
                "r",
            )
            print(os.path.basename(img_folder))
            data = dataf.readlines()
            data = [d.split(",") for d in data[1:]]
            for i in range(len(data)):
                for j in range(len(data[i])):
                    try:
                        data[i][j] = float(data[i][j])
                    except:
                        del data[i][j]
            for d in score(data):
                note(d)
            dataf.close()
            # input("Here")

            note(os.path.basename(img_folder).split("_")[1])

            note("\n")

        except KeyError:
            print(img_folder)
            note("\n")

        # input("here")


if __name__ == "__main__":
    get_info(args.img_path)
