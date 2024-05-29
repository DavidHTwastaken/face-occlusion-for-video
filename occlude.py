import cv2
import mediapipe as mp
import os

# Initialize MediaPipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils


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
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the BGR image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the frame and detect faces
            results = face_detection.process(rgb_frame)

            if results.detections:
                for detection in results.detections:
                    # Get the bounding box coordinates
                    bboxC = detection.location_data.relative_bounding_box
                    h, w, _ = frame.shape
                    x_min = int(bboxC.xmin * w)
                    y_min = int(bboxC.ymin * h)
                    box_width = int(bboxC.width * w)
                    box_height = int(bboxC.height * h)

                    # Draw a black rectangle over the face
                    cv2.rectangle(frame, (x_min, y_min), (x_min +
                                  box_width, y_min + box_height), (0, 0, 0), -1)

            # Write the frame to the output video
            if output_video_path:
                out.write(frame)

            if show:
                cv2.imshow('frame', frame)
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
