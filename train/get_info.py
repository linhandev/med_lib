import argparse
import os

import pydicom

parser = argparse.ArgumentParser()
parser.add_argument("--img_path", type=str, default="/home/lin/Desktop/data/aorta/10-24/dcm")
args = parser.parse_args()

f = open("header.csv", "w")


def note(info):
    if info == "\n":
        print(file=f)
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


def get_info(img_path):
    imgs = os.listdir(img_path)
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
        ]
    )

    for img_name in imgs:
        file_path = os.path.join(img_path, img_name)
        scan = os.listdir(file_path)[0]
        file_path = os.path.join(file_path, scan)

        hdr = pydicom.dcmread(os.path.join(img_path, file_path))

        print(
            "------------------------------------------------------------------------------------------------------------"
        )
        print(hdr)
        # input("here")
        print("\n\n\n\n\n")
        note(img_name.split("_")[0])
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

        note(img_name.split("_")[1])

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

        note("\n")
        # input("here")


if __name__ == "__main__":
    get_info(args.img_path)
