from occlude import occlude_faces
import argparse


def main():
    parser = argparse.ArgumentParser(description='Occlude faces in a video')
    parser.add_argument('--input', type=str,
                        help='Path to the input video file')
    parser.add_argument('--output', type=str,
                        help='Path to the output video file')
    parser.add_argument('--show', action='store_true',
                        help='Show the video while processing')
    args = parser.parse_args()

    occlude_faces(input_video_path=args.input,
                  output_video_path=args.output, show=args.show)


if __name__ == '__main__':
    main()
