import argparse
import os
from utils import process_videos, process_video, process_camera
from occlude import occlude_faces


def main():
    parser = argparse.ArgumentParser(description='Occlude faces in videos')
    parser.add_argument('--input', '-i', type=str, nargs='+',
                        help='Path to the input video file')
    parser.add_argument('--output', '-o', type=str,
                        help='Path to the output video file or directory')
    parser.add_argument('--suffix', '-s', type=str, default='_occluded',
                        help='Suffix to add to the output video file name')
    parser.add_argument('--show', action='store_true',
                        help='Show the video while processing')
    parser.add_argument('--keep-audio', action='store_true',
                        help='Keep the audio in the output video')
    args = parser.parse_args()

    # If no input files are provided, process the webcam feed
    if len(args.input) == 0 and args.show:
        process_camera(output=args.output, show=args.show)
    # Single file as input
    if len(args.input) == 1:
        if args.output == None:
            path, ext = os.path.splitext(args.input[0])
            output = f"{path}{args.suffix}{ext}"

        process_video(args.input[0], output,
                      keep_audio=args.keep_audio, show=args.show)
    # If there are multiple input files, output path should be a directory
    process_videos(args.input,
                   args.output, keep_audio=args.keep_audio,
                   show=args.show)


if __name__ == '__main__':
    main()
