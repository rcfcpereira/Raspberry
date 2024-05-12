import tkinter as tk
import time
import threading

import debug_files.gpio_lib as RaceGPIO
from picamera2 import Picamera2
from picamera2.encoders import MultiEncoder
import race_logging  # Import the race logging module

# Function to run camera recording in a thread
def run_camera(camera, filename):
    camera.start_and_record_video(filename)

class DragRaceGUI:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Drag Race GUI")
        
        self.info_label = tk.Label(self.master)
        self.info_label.pack()
        
        self.start_button = tk.Button(self.master, text="Start Race", command=self.start_race)
        self.start_button.pack()

        # Initialize GPIO and LCD
        self.gpio_race = RaceGPIO.RaceGPIO()
        #self.lcd_race = RaceLCD.RaceLCD()

        # Create image and draw of the display
        #self.image, self.draw = self.lcd_race.create_image()
        # Load fonts
        #self.fonts = self.lcd_race.create_fonts()

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
    
    def update_gui_info(self, message):
        self.info_label.config(text=message)

    def run_camera(self, camera, filename):
        camera.start_and_record_video(filename)

    def update_lcd_info(self, info):
        # Update the LCD information display
        self.lcd_info.config(text=info)
        self.master.update()

    def start_race(self):
        # Update the GUI information display
        self.update_gui_info("Starting race...")

        # Create and start the camera threads
        self.left_camera_thread.start()
        self.right_camera_thread.start()

        # self.left_camera_thread = Thread(target=self.left_camera.start)
        # self.right_camera_thread = Thread(target=self.right_camera.start)


        # Wait for the start button to be pressed
        while not self.gpio_race.turn_on_start_button_led():
            time.sleep(0.1)

        # Display a countdown on the GUI
        for i in range(3, 0, -1):
            countdown_message = f"Race starts in {i}"
            self.update_gui_info(countdown_message)
            time.sleep(1)

        # Start the race
        race_start_message = "Go!"
        self.update_gui_info(race_start_message)
        start_time = time.time()

        # Wait for either racer to cross the finish line or for the clock to exceed 90 seconds
        while time.time() - start_time < 90 and not self.gpio_race.finish_line_crossed():
            time.sleep(0.1)

        # Stop the cameras
        self.picam2_0.stop_video()
        self.picam2_1.stop_video()

        # Calculate and display the finish times
        finish_time = time.time() - start_time
        finish_message = f"Race finished in {finish_time} seconds"
        self.update_gui_info(finish_message)

        # Log the race data
        race_logging.log_race_data(start_time, finish_time)

def run_gui():
    root = tk.Tk()
    app = DragRaceGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()
