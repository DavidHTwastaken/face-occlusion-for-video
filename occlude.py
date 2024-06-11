import cv2
import os
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from mediapipe import solutions
from mediapipe.framework.formats import landmark_pb2
from mediapipe.python.solutions.drawing_utils import DrawingSpec
import numpy as np
import matplotlib.pyplot as plt
from draw_landmarks_modified import occlude_landmarks

mp_drawing = solutions.drawing_utils

BaseOptions = python.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

model_path = 'face_landmarker.task'

# Create a face landmarker instance with the video mode:
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.VIDEO)


def occlude_faces(input_video_path=None, output_video_path=None, show=True):
    # Open the input video
    cap = cv2.VideoCapture(input_video_path if input_video_path else 0)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    codec = cv2.VideoWriter_fourcc(*'XVID')

    # Initialize the VideoWriter for output video
    if output_video_path:
        out = cv2.VideoWriter(output_video_path, codec, fps,
                              (frame_width, frame_height))

    # Initialize MediaPipe face detection
    with FaceLandmarker.create_from_options(options) as landmarker:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert frame to MediaPipe Image object
            mp_image = mp.Image(
                image_format=mp.ImageFormat.SRGB, data=frame)

            # Get the current frame timestamp in milliseconds
            frame_timestamp_ms = int(cap.get(
                cv2.CAP_PROP_POS_MSEC))

            # Process the frame and detect face landmarks
            results = landmarker.detect_for_video(
                mp_image, frame_timestamp_ms)

            occluded_frame = np.copy(mp_image.numpy_view())
            if results.face_landmarks:
                for face_landmarks in results.face_landmarks:
                    face_landmarks_proto = landmark_pb2.NormalizedLandmarkList()
                    face_landmarks_proto.landmark.extend([
                        landmark_pb2.NormalizedLandmark(
                            x=landmark.x, y=landmark.y, z=landmark.z)
                        for landmark in face_landmarks
                    ])
                    # solutions.drawing_utils.draw_landmarks(
                    #     image=occluded_frame,
                    #     landmark_list=face_landmarks_proto,
                    #     connections=mp.solutions.face_mesh.FACEMESH_TESSELATION,
                    #     landmark_drawing_spec=None,
                    #     connection_drawing_spec=mp.solutions.drawing_styles
                    #     .get_default_face_mesh_tesselation_style())
                    occlude_landmarks(
                        image=occluded_frame,
                        landmark_list=face_landmarks_proto,
                        connections=mp.solutions.face_mesh.FACEMESH_LIPS,
                        connection_drawing_spec=DrawingSpec(
                            color=(0, 0, 0), thickness=1),
                        landmark_drawing_spec=None)

            # Write the frame to the output video
            if output_video_path:
                out.write(occluded_frame)

            if show:
                cv2.imshow('frame', occluded_frame)
                key = cv2.waitKey(1)

    # Release the video capture and writer objects
    cap.release()
    out.release()
    print(f"Processed video saved as {output_video_path}")


# Example usage
# From file
# occlude_faces(os.path.join('..', 'TestFiles', 'input.mkv'), 'output_video.mkv')

# From webcam
occlude_faces(show=True)
