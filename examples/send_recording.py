import socket
import time
import csv
from pylivelinkface import PyLiveLinkFace, FaceBlendShape

# Network settings
UDP_IP = "127.0.0.1"
UDP_PORT = 11111
frame_rate = 60

# CSV file path - update this to your file location
CSV_FILE_PATH = "../recording/recording.csv"



# Map CSV column names to FaceBlendShape enum values
blendshape_mapping = {
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

def read_csv_data(file_path):
    """Read CSV file and return a list of dictionaries with blendshape values"""
    data = []
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        for row in reader:
            data.append(row)
    return data

def main():
    # Initialize LiveLinkFace interface
    py_face = PyLiveLinkFace()
    
    try:
        # Read CSV data
        print(f"Reading blendshape data from {CSV_FILE_PATH}...")
        blendshape_data = read_csv_data(CSV_FILE_PATH)
        print(f"Loaded {len(blendshape_data)} frames of animation")
        
        # Create UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((UDP_IP, UDP_PORT))
        print(f"Connected to {UDP_IP}:{UDP_PORT}")
        
        # Process each frame of animation
        print("Starting animation playback...")
        frame_count = 0
        for frame in blendshape_data:
            frame_count += 1
            
            # Reset blendshapes for this frame
            py_face.reset_blendshapes()
            
            # Set all blendshapes from the CSV data
            for column_name, blendshape_enum in blendshape_mapping.items():
                if column_name in frame:
                    try:
                        value = float(frame[column_name])
                        py_face.set_blendshape(blendshape_enum, value)
                    except (ValueError, KeyError):
                        # Skip if conversion fails or key doesn't exist
                        pass
            
            # Send the frame
            s.sendall(py_face.encode())
            
            # Print progress every 100 frames
            if frame_count % 100 == 0:
                print(f"Sent frame {frame_count}/{len(blendshape_data)}")
                
            # Calculate frame timing based on timecode if available, otherwise use fixed rate
            if "Timecode" in frame and frame_count < len(blendshape_data):
                current_time = float(frame["Timecode"])
                next_time = float(blendshape_data[frame_count]["Timecode"])
                sleep_time = next_time - current_time
                if sleep_time > 0:
                    time.sleep(sleep_time)
            else:
                # Default to 30fps if timecode not available
                time.sleep(1/frame_rate)
                
        print("Animation playback completed")
                
    except KeyboardInterrupt:
        print("\nPlayback interrupted by user")
    except FileNotFoundError:
        print(f"Error: Could not find CSV file at {CSV_FILE_PATH}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        s.close()
        print("Connection closed")

if __name__ == "__main__":
    main()