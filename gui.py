import tkinter as tk
from tkinter import filedialog, Tk, StringVar
from tkinter import ttk


class App(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.config(padding=10)
        self.pack()

        self.selected_files_var = StringVar()
        self.selected_files_count = StringVar()

        # Label
        label = ttk.Label(self, text="Occlude Faces in Video")
        label.pack()
        # Input files button
        button = ttk.Button(self, text="Select input videos",
                            command=self.select_videos)
        button.pack()
        # Input files list
        self.input_files = ttk.Entry(
            self, width=50, textvariable=self.selected_files_var, state='readonly')
        self.input_files.pack()
        number_of_files = ttk.Label(
            self, textvariable=self.selected_files_count)
        number_of_files.pack()

    def select_videos(self):
        selected_files = filedialog.askopenfilenames(
            filetypes=[("Video files", "*.mp4")])
        text = ', '.join(
            selected_files) if selected_files else "No files selected"
        self.selected_files_var.set(text)
        self.selected_files_count.set(
            f"Number of files: {len(selected_files)}")


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
