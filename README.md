
# Face Occlusion for Videos

This project provides a command-line program and a GUI for occluding facial features in videos. The goal was to create a simple tool that allows for partial occlusion based on facial regions (e.g. eyes, mouth, nose) and facilitates the processing of many videos in a batch.
## Installation

Clone this repository and install the python dependencies, preferably to a virtual environment.

```
    git clone https://github.com/DavidHTwastaken/face-occlusion-for-video.git
    cd face-occlusion-for-video
    pip install -r requirements.txt
```
    
## Usage/Examples

Occlude whole faces (default behavior) in video files `file1.mp4` and `file2.mp4`, and store the results in the directory called `output_dir`:

`python cli.py -i file1.mp4 file2.mp4 -o output_dir -f f`


## Demo


