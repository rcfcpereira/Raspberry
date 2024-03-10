import tkinter as tk
import os
import sys
import time
import threading

import gpio_lib as RaceGPIO
import lcd_lib as RaceLCD
from PIL import Image
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
import race_logging  # Import the race logging module

class DragRaceGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Drag Race GUI")
        
        self.start_button = tk.Button(self.master, text="Start Race", command=self.start_race)
        self.start_button.pack()

        # Initialize GPIO and LCD
        self.gpio_race = RaceGPIO.RaceGPIO()
        self.lcd_race = RaceLCD.RaceLCD()

        # Create image and draw of the display
        self.image, self.draw = self.lcd_race.create_image()
        # Load fonts
        self.fonts = self.lcd_race.create_fonts()

        # Set up cameras and configurations (as in your existing code)
        self.picam2_0 = Picamera2(0)
        self.picam2_1 = Picamera2(1)
        self.encoder = MultiEncoder()

        # Configure cameras (as in your existing code)
        self.config_0 = self.picam2_0.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})
        self.config_1 = self.picam2_1.create_video_configuration(main={"size": (640, 480), "format": "RGB888"}, controls={'FrameRate': 200})

        self.picam2_0.configure(self.config_0)
        self.picam2_1.configure(self.config_1)

        # Start Camera Threads (as in your existing code)
        self.left_camera_thread = threading.Thread(target=self.run_camera, args=(self.picam2_0, "left_track_race1.mp4"))
        self.right_camera_thread = threading.Thread(target=self.run_camera, args=(self.picam2_1, "right_track_race1.mp4"))

    def run_camera(self, camera, filename):
        camera.start_and_record_video(filename)

    def start_race(self):
        # Add your existing race logic here
        print("Starting race...")
        # For example, you could start camera threads and other race preparations here

        # Start the camera threads
        self.left_camera_thread.start()
        self.right_camera_thread.start()

def run_gui():
    root = tk.Tk()
    app = DragRaceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
