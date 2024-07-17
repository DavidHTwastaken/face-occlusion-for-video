from occlude import occlude_faces, integrate_audio
import argparse


def main():
    parser = argparse.ArgumentParser(description='Occlude faces in a video')
    parser.add_argument('--input', type=str,
                        help='Path to the input video file')
    parser.add_argument('--output', type=str,
                        help='Path to the output video file')
    parser.add_argument('--show', action='store_true',
                        help='Show the video while processing')
    parser.add_argument('--keep-audio', action='store_true',
                        help='Keep the audio in the output video')
    args = parser.parse_args()

    occlude_faces(input_video_path=args.input,
                  output_video_path=args.output, show=args.show)
    integrate_audio(args.input, args.output)


if __name__ == '__main__':
    main()
