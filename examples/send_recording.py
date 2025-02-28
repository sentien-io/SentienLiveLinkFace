import csv
import socket
import time
from pylivelinkface import PyLiveLinkFace, FaceBlendShape

UDP_IP = "127.0.0.1"
UDP_PORT = 11111
CSV_FILE = "../recording/recording.csv"  # Change this to your actual CSV file

# Map each CSV column to its corresponding FaceBlendShape
COLUMN_TO_BLENDSHAPE = {
    "EyeBlinkLeft": FaceBlendShape.EyeBlinkLeft,
    "EyeLookDownLeft": FaceBlendShape.EyeLookDownLeft,
    "EyeLookInLeft": FaceBlendShape.EyeLookInLeft,
    "EyeLookOutLeft": FaceBlendShape.EyeLookOutLeft,
    "EyeLookUpLeft": FaceBlendShape.EyeLookUpLeft,
    "EyeSquintLeft": FaceBlendShape.EyeSquintLeft,
    "EyeWideLeft": FaceBlendShape.EyeWideLeft,
    "EyeBlinkRight": FaceBlendShape.EyeBlinkRight,
    "EyeLookDownRight": FaceBlendShape.EyeLookDownRight,
    "EyeLookInRight": FaceBlendShape.EyeLookInRight,
    "EyeLookOutRight": FaceBlendShape.EyeLookOutRight,
    "EyeLookUpRight": FaceBlendShape.EyeLookUpRight,
    "EyeSquintRight": FaceBlendShape.EyeSquintRight,
    "EyeWideRight": FaceBlendShape.EyeWideRight,
    "JawForward": FaceBlendShape.JawForward,
    "JawRight": FaceBlendShape.JawRight,
    "JawLeft": FaceBlendShape.JawLeft,
    "JawOpen": FaceBlendShape.JawOpen,
    "MouthClose": FaceBlendShape.MouthClose,
    "MouthFunnel": FaceBlendShape.MouthFunnel,
    "MouthPucker": FaceBlendShape.MouthPucker,
    "MouthRight": FaceBlendShape.MouthRight,
    "MouthLeft": FaceBlendShape.MouthLeft,
    "MouthSmileLeft": FaceBlendShape.MouthSmileLeft,
    "MouthSmileRight": FaceBlendShape.MouthSmileRight,
    "MouthFrownLeft": FaceBlendShape.MouthFrownLeft,
    "MouthFrownRight": FaceBlendShape.MouthFrownRight,
    "MouthDimpleLeft": FaceBlendShape.MouthDimpleLeft,
    "MouthDimpleRight": FaceBlendShape.MouthDimpleRight,
    "MouthStretchLeft": FaceBlendShape.MouthStretchLeft,
    "MouthStretchRight": FaceBlendShape.MouthStretchRight,
    "MouthRollLower": FaceBlendShape.MouthRollLower,
    "MouthRollUpper": FaceBlendShape.MouthRollUpper,
    "MouthShrugLower": FaceBlendShape.MouthShrugLower,
    "MouthShrugUpper": FaceBlendShape.MouthShrugUpper,
    "MouthPressLeft": FaceBlendShape.MouthPressLeft,
    "MouthPressRight": FaceBlendShape.MouthPressRight,
    "MouthLowerDownLeft": FaceBlendShape.MouthLowerDownLeft,
    "MouthLowerDownRight": FaceBlendShape.MouthLowerDownRight,
    "MouthUpperUpLeft": FaceBlendShape.MouthUpperUpLeft,
    "MouthUpperUpRight": FaceBlendShape.MouthUpperUpRight,
    "BrowDownLeft": FaceBlendShape.BrowDownLeft,
    "BrowDownRight": FaceBlendShape.BrowDownRight,
    "BrowInnerUp": FaceBlendShape.BrowInnerUp,
    "BrowOuterUpLeft": FaceBlendShape.BrowOuterUpLeft,
    "BrowOuterUpRight": FaceBlendShape.BrowOuterUpRight,
    "CheekPuff": FaceBlendShape.CheekPuff,
    "CheekSquintLeft": FaceBlendShape.CheekSquintLeft,
    "CheekSquintRight": FaceBlendShape.CheekSquintRight,
    "NoseSneerLeft": FaceBlendShape.NoseSneerLeft,
    "NoseSneerRight": FaceBlendShape.NoseSneerRight,
    "TongueOut": FaceBlendShape.TongueOut,
    "HeadYaw": FaceBlendShape.HeadYaw,
    "HeadPitch": FaceBlendShape.HeadPitch,
    "HeadRoll": FaceBlendShape.HeadRoll,
    "LeftEyeYaw": FaceBlendShape.LeftEyeYaw,
    "LeftEyePitch": FaceBlendShape.LeftEyePitch,
    "LeftEyeRoll": FaceBlendShape.LeftEyeRoll,
    "RightEyeYaw": FaceBlendShape.RightEyeYaw,
    "RightEyePitch": FaceBlendShape.RightEyePitch,
    "RightEyeRoll": FaceBlendShape.RightEyeRoll
}

def main():
    py_face = PyLiveLinkFace()

    # Read all rows from the CSV
    with open(CSV_FILE, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((UDP_IP, UDP_PORT))

        for row in rows:
            for col_name, blendshape in COLUMN_TO_BLENDSHAPE.items():
                if col_name in row:
                    value = float(row[col_name])
                    py_face.set_blendshape(blendshape, value)
            s.sendall(py_face.encode())
            time.sleep(0.1)  # Adjust based on the frame rate of your animation

    except KeyboardInterrupt:
        pass
    finally:
        s.close()

if __name__ == "__main__":
    main()
