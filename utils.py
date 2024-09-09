import os
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from occlude import occlude_faces, integrate_audio
import time


class ProcessResults:
    def __init__(self):
        self.total_duration: float = None
        self.output_files = []


def parse_settings():
    settings = {}
    with open(".settings") as myfile:
        for line in myfile:
            name, var = line.split("=")
            settings[name.strip()] = var.strip()
    return settings


SETTINGS = parse_settings()
VALID_FILE_EXTENSION = '.mp4'


def ask_for_file_path() -> str:
    filename = askopenfilename()
    return filename


def make_video_copies(video_path, num_copies, file_path_prefix=""):
    file_name, file_extension = os.path.splitext(video_path)
    for i in range(num_copies):
        new_file_name = f"{file_path_prefix}{file_name}_copy_{i+1}{file_extension}"
        shutil.copy2(video_path, new_file_name)
        print(f"Copy {i+1} created: {new_file_name}")


def handle_video_processing(suffix="", count_time=False):
    files = askopenfilename(initialdir='.', multiple=True)
    output_folder = askdirectory(initialdir='.')
    return process_videos(files, output_folder, suffix, count_time)


def process_videos(files, output_folder, suffix="", count_time=False, keep_audio=False, show=False):
    results = ProcessResults()
    if count_time:
        results.total_duration = 0
    for index, filepath in enumerate(files):
        if count_time:
            start_time = time.time()
        print(f"Processing file {index+1} of {len(files)}")
        file = os.path.basename(filepath)
        filename, file_extension = os.path.splitext(file)
        output_path = os.path.join(
            output_folder, f'{filename}{suffix}{VALID_FILE_EXTENSION}')
        print(output_path)
        occlude_faces(input_video_path=filepath,
                      output_video_path=output_path, show=show)
        if keep_audio:
            integrate_audio(filepath, output_path)
        if count_time:
            time_taken = time.time() - start_time
            results.total_duration += time_taken
            print(f"Time taken to process video: {time_taken} seconds")
    print(f"All videos processed and can be found in: {output_folder}")
    return results


def process_video(input: str, output: str, keep_audio=False, show=False):
    occlude_faces(input_video_path=input, output_video_path=output, show=show)
    if keep_audio:
        integrate_audio(input, output)


def process_camera(output=None, show=False):
    occlude_faces(output_video_path=output, show=show)
    # TODO: Figure out how to get audio from camera feed
    # if keep_audio:
    #     integrate_audio(output, output)


def main():
    # video_path = ask_for_file_path()
    # num_copies = int(input("Enter the number of copies you want to create: "))
    # make_video_copies(video_path, num_copies)
    results = process_videos(count_time=True)
    print(
        "Total time taken to process all videos: " +
        f"{time.strftime('%H:%M:%S', time.gmtime(results.total_duration))}")


if __name__ == '__main__':
    main()
