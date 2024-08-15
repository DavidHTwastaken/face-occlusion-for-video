import argparse
import os
from utils import process_videos
from occlude import occlude_faces


def main():
    parser = argparse.ArgumentParser(description='Occlude faces in videos')
    parser.add_argument('--input', '-i', type=str, nargs='+',
                        help='Path to the input video file')
    parser.add_argument('--output', '-o', type=str,
                        help='Path to the output video file')
    parser.add_argument('--suffix', '-s', type=str,
                        help='Suffix to add to the output video file name')
    parser.add_argument('--show', action='store_true',
                        help='Show the video while processing')
    parser.add_argument('--keep-audio', action='store_true',
                        help='Keep the audio in the output video')
    args = parser.parse_args()

    # If there are multiple input files, output path should be a directory
    if len(args.input) == 0:
        occlude_faces(output_video_path=args.output,
                      show=args.show, keep_audio=args.keep_audio)
    if len(args.input) == 1:
        if args.output == None:
            os.path.splitext(args.input[0])
            args.output = args.input[0].split('.')

    process_videos(args.input,
                   args.output, keep_audio=args.keep_audio,
                   show=args.show)


if __name__ == '__main__':
    main()
