from tkinter import *
from pathlib import Path
import imageio
from PIL import ImageTk, Image

# Test constants
VIDEO_NAME = Path().absolute() / "media/videos/bubblesort/480p15/BubbleSortScene.mp4"
VIDEO = imageio.get_reader(VIDEO_NAME)
VIDEO_DELAY = int(1000 / VIDEO.get_meta_data()['fps'])


class VideoGUI:
    def __init__(self):
        self.root = Tk()

        self.video_window = Label(self.root)
        self.video_window.pack(side=TOP)

        button_frame = Frame(self.root)
        button_frame.pack(side=BOTTOM)

        self.pause = False   # Parameter that controls pause button

        # Play button
        self.btn_play=Button(button_frame, 
                             text="Play", width=15, command=self.play_video)
        self.btn_play.grid(row=0, column=0)

        # Pause button
        self.btn_pause=Button(button_frame, 
                              text="Pause", width=15, command=self.pause_video)
        self.btn_pause.grid(row=0, column=1)

        self.show_video_start()
        self.root.mainloop()
    
    def pause_video(self):
        self.pause = True

    def show_video_start(self):
        try:
            image = VIDEO.get_next_data()
        except:
            VIDEO.close()
            return
        frame_image = ImageTk.PhotoImage(Image.fromarray(image))
        self.video_window.config(image=frame_image)
        self.video_window.image = frame_image

    def play_video(self):
        if self.pause:
            self.pause = False
            self.root.after_cancel(self.after_id)
        else:
            try:
                image = VIDEO.get_next_data()
            except:
                VIDEO.close()
                return
            self.after_id = self.root.after(VIDEO_DELAY, self.play_video)

            frame_image = ImageTk.PhotoImage(Image.fromarray(image))
            self.video_window.config(image=frame_image)
            self.video_window.image = frame_image


if __name__ == '__main__':
    VideoGUI()
