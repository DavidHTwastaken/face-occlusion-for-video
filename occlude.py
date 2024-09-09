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
from moviepy.editor import VideoFileClip


mp_drawing = solutions.drawing_utils

BaseOptions = python.BaseOptions
FaceLandmarker = mp.tasks.vision.FaceLandmarker
FaceLandmarkerOptions = mp.tasks.vision.FaceLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

MODEL_PATH = 'face_landmarker.task'

# Create a face landmarker instance with the video mode:
options = FaceLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO)

# Mapping of keywords to MediaPipe face mesh features
feature_dict = {
    "face": mp.solutions.face_mesh.FACEMESH_TESSELATION,
    "lips": mp.solutions.face_mesh.FACEMESH_LIPS,
    "left_eye": mp.solutions.face_mesh.FACEMESH_LEFT_EYE,
    "right_eye": mp.solutions.face_mesh.FACEMESH_RIGHT_EYE,
    "left_eyebrow": mp.solutions.face_mesh.FACEMESH_LEFT_EYEBROW,
    "right_eyebrow": mp.solutions.face_mesh.FACEMESH_RIGHT_EYEBROW,
    "left_pupil": mp.solutions.face_mesh.FACEMESH_LEFT_IRIS,
    "right_pupil": mp.solutions.face_mesh.FACEMESH_RIGHT_IRIS,
    "nose": mp.solutions.face_mesh.FACEMESH_NOSE,
    "oval": mp.solutions.face_mesh.FACEMESH_FACE_OVAL
}


def occlude_faces(input_video_path: str = None, output_video_path: str = None, show=False, hints=False):
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

    if show and hints:
        print("Press 'f' to toggle face landmarks")
        print("Press 'l' to toggle lips landmarks")
        print("Press 'e' to toggle eye landmarks")
        print("Press 'n' to toggle nose landmarks")
        print("Press 'o' to toggle oval landmarks")
        print("Press 'q' to quit")

    # Initialize MediaPipe face detection
    with FaceLandmarker.create_from_options(options) as landmarker:
        selected_features = {"face"}
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
                    for feature in selected_features:
                        occlude_landmarks(
                            image=occluded_frame,
                            landmark_list=face_landmarks_proto,
                            connections=feature_dict[feature],
                            connection_drawing_spec=DrawingSpec(
                                color=(0, 0, 0), thickness=1),
                            landmark_drawing_spec=None)

            # Write the frame to the output video
            if output_video_path:
                out.write(occluded_frame)

            if show:
                cv2.imshow('frame', occluded_frame)
                key = cv2.waitKey(1)
                if key == ord('q'):
                    break

                def toggle_feature(feature):
                    if feature in selected_features:
                        selected_features.remove(feature)
                    else:
                        selected_features.add(feature)

                if key == ord('f'):
                    toggle_feature("face")
                if key == ord('l'):
                    toggle_feature("lips")
                if key == ord('e'):
                    toggle_feature("left_eye")
                    toggle_feature("right_eye")
                if key == ord('n'):
                    toggle_feature("nose")
                if key == ord('o'):
                    toggle_feature("oval")

    # Release the video capture and writer objects
    cap.release()
    if output_video_path:
        out.release()
        print(f"Processed video saved as {output_video_path}")


def integrate_audio(original_video: str, output_video: str, audio_path=os.path.join('tmp', 'audio.mp3')):
    '''
    Extracts audio from the original video and integrates it into the output video. This
    function was copied from the AWS Rekognition Video People Blurring CDK project. \n
    Source:  https://github.com/aws-samples/rekognition-video-people-blurring-cdk/blob/main/stack/lambdas/rekopoc-apply-faces-to-video-docker/video_processor.py
    '''
    # Extract audio
    my_clip = VideoFileClip(original_video)
    my_clip.audio.write_audiofile(audio_path)
    print('finished writing audio to temp file')
    temp_location = os.path.join('tmp', 'output_video.mp4')
    # Join output video with extracted audio
    videoclip = VideoFileClip(output_video)
    videoclip.write_videofile(
        temp_location, codec='libx264', audio=audio_path, audio_codec='libmp3lame')

    os.rename(temp_location, output_video)
    # Delete audio
    os.remove(audio_path)

# Example usage
# From file
# occlude_faces(os.path.join('..', 'TestFiles', 'input.mkv'), 'output_video.mkv')

# From webcam
# occlude_faces(show=True)
