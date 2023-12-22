import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import sys
import asyncio
import logging
from bleak import BleakClient, BleakScanner

ADDRESS = "84:FC:E6:00:B7:66"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class ImageProcessorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Processor")

        # Initialize variables
        self.image_list = []
        self.current_image_index = 0

        # Create GUI components
        self.label = tk.Label(self.master)
        self.label.pack(expand=True, fill="both")

        self.zoom_in_button = tk.Button(self.master, text="Zoom In", command=self.zoom_in)
        self.zoom_in_button.pack(side="left")

        self.zoom_out_button = tk.Button(self.master, text="Zoom Out", command=self.zoom_out)
        self.zoom_out_button.pack(side="left")

        self.next_button = tk.Button(self.master, text="Next", command=self.next_image)
        self.next_button.pack(side="left")

        self.prev_button = tk.Button(self.master, text="Previous", command=self.prev_image)
        self.prev_button.pack(side="left")

        self.rotate_left_button = tk.Button(self.master, text="Rotate Left", command=self.rotate_left)
        self.rotate_left_button.pack(side="left")

        self.rotate_right_button = tk.Button(self.master, text="Rotate Right", command=self.rotate_right)
        self.rotate_right_button.pack(side="left")

        self.load_image_button = tk.Button(self.master, text="Load Image", command=self.load_image)
        self.load_image_button.pack(side="left")

        # Initialize BLE variables
        self.ble_client = BleakClient(ADDRESS)
        self.connect_ble()  # Start BLE communication in parallel

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*")])
        if file_path:
            print("Selected file:", file_path)  # Print the selected file path for debugging
            try:
                image = cv2.imread(file_path)
                if image is not None:
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    self.image_list.append(image_rgb)
                    self.current_image_index = len(self.image_list) - 1
                    self.update_display()
                else:
                    print("Error: Unable to read the image.")
            except Exception as e:
                print("Error loading image:", str(e))

    def update_display(self):
        if self.image_list and 0 <= self.current_image_index < len(self.image_list):
            current_image = self.image_list[self.current_image_index]
            image = Image.fromarray(current_image)
            photo = ImageTk.PhotoImage(image)
            self.label.config(image=photo)
            self.label.image = photo

    def zoom_in(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            zoomed_image = cv2.resize(current_image, (int(current_image.shape[1] * 1.2), int(current_image.shape[0] * 1.2)))
            self.image_list[self.current_image_index] = zoomed_image
            self.update_display()

    def zoom_out(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            zoomed_image = cv2.resize(current_image, (int(current_image.shape[1] / 1.2), int(current_image.shape[0] / 1.2)))
            self.image_list[self.current_image_index] = zoomed_image
            self.update_display()

    def next_image(self):
        if self.image_list:
            if self.current_image_index < len(self.image_list) - 1:
                self.current_image_index += 1
                self.update_display()

    def prev_image(self):
        if self.image_list:
            if self.current_image_index > 0:
                self.current_image_index -= 1
                self.update_display()

    def rotate_left(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            rotated_image = cv2.rotate(current_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            self.image_list[self.current_image_index] = rotated_image
            self.update_display()

    def rotate_right(self):
        if self.image_list:
            current_image = self.image_list[self.current_image_index]
            rotated_image = cv2.rotate(current_image, cv2.ROTATE_90_CLOCKWISE)
            self.image_list[self.current_image_index] = rotated_image
            self.update_display()

    def connect_ble(self):
        async def ble_task():
            try:
                device = await BleakScanner.find_device_by_address(ADDRESS)
                if device is None:
                    logging.error(f"Could not find device with address {ADDRESS}")
                    return
                else:
                    logging.info(f"Device found with address {ADDRESS}")

                await self.ble_client.connect()
                logging.info(f"Connected: {self.ble_client.is_connected}")

                while True:
                    data_bytes = await self.ble_client.read_gatt_char(CHARACTERISTIC_UUID)
                    data = bytearray.decode(data_bytes)
                    logging.info(f"Received data: {data}")
                    # Call Function here with data as an argument
                    await asyncio.sleep(1)

            except KeyboardInterrupt:
                logging.info("Script interrupted by user.")
            except Exception as e:
                logging.error(f"Error: {e}")
            finally:
                if self.ble_client.is_connected:
                    await self.ble_client.disconnect()
                    logging.info("Disconnected.")

        asyncio.create_task(ble_task())

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
