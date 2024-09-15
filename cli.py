import argparse
import os
from utils import process_videos, process_video, process_camera


def get_features(features):
    feature_map = {
        'e': ['left_eye', 'right_eye'],
        'm': ['lips'],
        'n': ['nose'],
        'f': ['face']
    }
    feature_list = []
    for feature in features:
        if feature in feature_map:
            feature_list.extend(feature_map[feature])
        else:
            feature_list.extend(feature)
    return set(feature_list)


def main():
    parser = argparse.ArgumentParser(description='Occlude faces in videos')
    parser.add_argument('--input', '-i', type=str, nargs='+',
                        help='Path to the input video file; if no input files are provided, \
                        the webcam feed will be used')
    parser.add_argument('--output', '-o', type=str,
                        help='Path to the output video file or directory')
    parser.add_argument('--suffix', '-s', type=str, default='_occluded',
                        help='Characters to append to the output video file name')
    parser.add_argument('--show', action='store_true',
                        help='Show the video while processing')
    parser.add_argument('--keep-audio', action='store_true',
                        help='Keep the audio in the output video')
    parser.add_argument('--features', '-f', type=str, nargs='+', default=['f'],
                        help='Features to occlude. Options: eyes (e), mouth (m), nose (n), whole face (f). Defaults to whole face.')
    args = parser.parse_args()

    features = get_features(args.features)
    # If no input files are provided, process the webcam feed
    if args.input == None:
        return process_camera(output=args.output, show=args.show, features=features)
    # Single file as input
    if len(args.input) == 1:
        output = args.output
        if output == None:
            path, ext = os.path.splitext(args.input[0])
            output = f"{path}{args.suffix}{ext}"
        elif os.path.isdir(output):
            basename = os.path.basename(args.input[0])
            filename, ext = os.path.splitext(basename)
            output = os.path.join(output, f'{filename}{args.suffix}{ext}')
        return process_video(args.input[0], output,
                             keep_audio=args.keep_audio, show=args.show, features=features)
    # If there are multiple input files, output path should be a directory
    return process_videos(args.input,
                          args.output, keep_audio=args.keep_audio, suffix=args.suffix,
                          show=args.show, features=features)


if __name__ == '__main__':
    main()
