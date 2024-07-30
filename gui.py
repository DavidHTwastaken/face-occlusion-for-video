import tkinter as tk
from tkinter import filedialog, Tk, StringVar
from tkinter import ttk
from utils import process_videos


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(padding=10)
        self.pack()

        self.selected_files = []
        self.selected_files_var = StringVar()
        self.selected_files_count = StringVar()
        self.selected_output_dir = StringVar()

        # Label
        label = ttk.Label(self, text="Occlude Faces in Video")
        label.pack()
        # Input files button
        input_files_button = ttk.Button(self, text="Select input videos",
                                        command=self.select_videos)
        input_files_button.pack()
        # Input files list
        self.input_files = ttk.Entry(
            self, width=50, textvariable=self.selected_files_var, state='readonly')
        self.input_files.pack()
        number_of_files = ttk.Label(
            self, textvariable=self.selected_files_count)
        number_of_files.pack()
        # Output directory button
        output_dir_button = ttk.Button(self, text="Select output directory",
                                       command=self.select_output_dir)
        output_dir_button.pack()
        # Output directory
        self.output_dir = ttk.Entry(
            self, width=50, state='readonly', textvariable=self.selected_output_dir)
        self.output_dir.pack()
        # Occlude videos button
        occlude_button = ttk.Button(self, text="Occlude faces",
                                    command=lambda: process_videos(self.selected_files,
                                                                   self.selected_output_dir.get()))
        occlude_button.pack()

    def select_videos(self):
        self.selected_files = filedialog.askopenfilenames(
            filetypes=[("Video files", "*.mp4")])
        text = ', '.join(
            self.selected_files) if self.selected_files else "No files selected"
        self.selected_files_var.set(text)
        self.selected_files_count.set(
            f"Number of files: {len(self.selected_files)}")

    def select_output_dir(self):
        selected_dir = filedialog.askdirectory()
        self.selected_output_dir.set(selected_dir)


def main():
    # Root
    root = Tk()
    root.title("Occlude Faces in Video")
    root.geometry("400x200")
    # Main frame
    app = App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
