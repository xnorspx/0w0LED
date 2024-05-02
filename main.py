import tkinter as tk
from tkinter import colorchooser, simpledialog, filedialog
import os


class LEDMatrixApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LED Matrix Animation")

        # Create canvas for LED matrix
        self.canvas = tk.Canvas(root, width=24*20, height=32*20, bg="black")
        self.canvas.grid(row=0, column=1, columnspan=2)

        # Initialize selected color
        self.selected_color = "#FFFFFF"

        # Create a frame to group the color button and the color display box
        self.color_frame = tk.Frame(root)
        self.color_frame.grid(row=0, column=3, padx=10)

        # Color selection button
        self.color_button = tk.Button(self.color_frame, text="Select Color", command=self.choose_color)
        self.color_button.pack()

        # Display selected color box
        self.color_box = tk.Label(self.color_frame, bg=self.selected_color, width=5, height=1)
        self.color_box.pack()

        # Duration entry
        self.duration_label = tk.Label(root, text="Duration (ms):")
        self.duration_label.grid(row=1, column=1, sticky="e")

        self.duration_entry = tk.Entry(root)
        self.duration_entry.grid(row=1, column=2, pady=10)

        # Image list (on the left, within a frame)
        self.image_list_frame = tk.Frame(root)
        self.image_list_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")

        self.image_list_label = tk.Label(self.image_list_frame, text="Image List")
        self.image_list_label.pack()

        self.image_list = tk.Listbox(self.image_list_frame)
        self.image_list.pack(fill=tk.BOTH, expand=True)
        self.image_list.insert(tk.END, "Default")  # Initial canvas name

        # Add and Delete buttons (inside the frame)
        self.add_button = tk.Button(self.image_list_frame, text="Add", command=self.add_image)
        self.delete_button = tk.Button(self.image_list_frame, text="Delete", command=self.delete_image)
        self.add_button.pack(side=tk.LEFT, padx=5)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        # Save and Load button
        self.io_frame = tk.Frame(root)
        self.io_frame.grid(row=2, column=1, rowspan=2, padx=10, pady=10, sticky="ns")
        self.save_button = tk.Button(self.io_frame, text="Save", command=self.save_animation)
        self.save_button.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="ns")
        self.load_button = tk.Button(self.io_frame, text="Load", command=self.load_animation)
        self.load_button.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="ns")

        # Initialize image data (empty canvas)
        self.image_data = {"Default": {"name": "Default", "duration": 1000, "pixels": [["#000000"] * 24 for _ in range(32)]}}  # 24x32 canvas with all black pixels

        # Bind double-click event to image list
        self.image_list.bind("<Button-1>", self.select_image)
        self.image_list.bind("<Double-Button-1>", self.select_image)

        # Bind right-click event to image list
        self.image_list.bind("<Button-3>", self.rename_image)

        # Automatically select the Default image
        self.image_list.selection_set(0)

        # Update canvas with the Default image data
        self.update_canvas(0)

        # Add an "Update Duration" button
        self.update_duration_button = tk.Button(root, text="Update Duration", command=self.update_duration)
        self.update_duration_button.grid(row=1, column=3, padx=10)

        # Bind mouse events to canvas
        self.canvas.bind("<Button-1>", self.update_pixel_color)
        self.canvas.bind("<B1-Motion>", self.update_pixel_color)
        self.canvas.bind("<Button-3>", self.rm_pixel_color)
        self.canvas.bind("<B3-Motion>", self.rm_pixel_color)

    def choose_color(self):
        _, color = colorchooser.askcolor()
        if color:
            self.selected_color = color
            self.color_box.config(bg=self.selected_color)  # Update the color display box

    def update_pixel_color(self, event):
        # Handle user interaction on the canvas
        x, y = event.x // 20, event.y // 20
        if 0 <= x < 24 and 0 <= y < 32:
            selected_index = self.image_list.curselection()
            if selected_index:
                current_image = self.image_list.get(selected_index[0])
                self.image_data[current_image]["pixels"][y][x] = f"#{self.selected_color[1:]}"  # Convert to hex format
                self.update_canvas(selected_index[0], y, x)


    def rm_pixel_color(self, event):
        # Handle user interaction on the canvas
        x, y = event.x // 20, event.y // 20
        if 0 <= x < 24 and 0 <= y < 32:
            selected_index = self.image_list.curselection()
            if selected_index:
                current_image = self.image_list.get(selected_index[0])
                self.image_data[current_image]["pixels"][y][x] = f"#000000"  # Convert to hex format
                self.update_canvas(selected_index[0], y, x)

    def add_image(self):
        # Add a new canvas (image) to the list
        new_name = simpledialog.askstring("Add Image", "Enter a name for the new image:")
        if new_name:
            if new_name in self.image_data:
                tk.messagebox.showerror("Error", f"'{new_name}' already exists. Please choose a unique name.")
            else:
                duration = 50
                if duration is not None:
                    # Initialize the new image as an empty canvas (all black pixels)
                    self.image_list.insert(tk.END, new_name)
                    self.image_data[new_name] = {"name": new_name, "duration": duration,
                                                 "pixels": [["#000000"] * 24 for _ in range(32)]}
                    # Automatically select the newly added image
                    self.image_list.selection_clear(0, tk.END)  # Deselect all
                    self.image_list.selection_set(tk.END)  # Select the last item (newly added)
                    self.update_canvas(len(self.image_data) - 1)  # Update canvas with the new image data

    def delete_image(self):
        # Delete the selected canvas from the list
        selected_index = self.image_list.curselection()
        if selected_index:
            index = selected_index[0]
            self.image_list.delete(index)
            del self.image_data[index]

    def select_image(self, event):
        # Handle double-click on an image in the list
        selected_index = self.image_list.curselection()
        if selected_index:
            # Update canvas with selected image data
            self.update_canvas(selected_index[0])

            # Update the duration entry with the selected image's duration
            current_image = self.image_list.get(selected_index[0])
            self.duration_entry.delete(0, tk.END)
            self.duration_entry.insert(0, str(self.image_data[current_image]["duration"]))

    def rename_image(self, event):
        # Handle right-click on an image in the list
        selected_index = self.image_list.curselection()
        if selected_index:
            current_name = self.image_list.get(selected_index[0])
            new_name = simpledialog.askstring("Rename Image", f"Enter new name for '{current_name}':")
            if new_name:
                # Check for uniqueness
                if new_name in self.image_data:
                    tk.messagebox.showerror("Error", f"'{new_name}' already exists. Please choose a unique name.")
                else:
                    # Update list item
                    self.image_list.delete(selected_index)
                    self.image_list.insert(selected_index, new_name)

                    # Update image data
                    self.image_data[new_name] = self.image_data.pop(current_name)

    def save_animation(self):
        # Save animation data to a file
        filename = simpledialog.askstring("Save Animation", "Enter a filename for saving the animation:")
        if filename:
            with open(filename, "w") as file:
                for image_name, image_info in self.image_data.items():
                    row_strings = [";".join(row).replace("#", "") for row in image_info["pixels"]]
                    image_line = f"{image_name},{image_info['duration']},{';'.join(row_strings)}"
                    file.write(image_line + "\n")

    def load_animation(self):
        # Load animation data from a file
        filename = filedialog.askopenfilename(title="Animation", initialdir=os.getcwd())
        if filename:
            self.image_data.clear()
            with open(filename, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    image_name, duration, pixel_data = parts[0], int(parts[1]), parts[2:]
                    pixel_data = pixel_data[0].split(";")
                    pixels = []
                    count = 0
                    for y in range(32):
                        row = []
                        for x in range(24):
                            print(count)
                            row.append("#"+pixel_data[count])
                            count += 1
                        pixels.append(row)
                    self.image_data[image_name] = {"name": image_name, "duration": duration, "pixels": pixels}
                    print(pixels)
            # Update image list and canvas
            self.image_list.delete(0, tk.END)
            for image_name in self.image_data:
                self.image_list.insert(tk.END, image_name)
            # Automatically select the Default image
            self.image_list.selection_set(0)
            self.update_canvas(0)  # Display the first image

    def update_canvas(self, index, y = None, x = None):
        if y is None or x is None:
            for y in range(32):
                for x in range(24):
                    self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20,
                                                 fill=self.image_data[self.image_list.get(index)]["pixels"][y][x])
        else:
            # Update canvas with pixel colors from the selected image data
            self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill=self.image_data[self.image_list.get(index)]["pixels"][y][x])

    def update_duration(self):
        # Update the duration of the selected image
        selected_index = self.image_list.curselection()
        if selected_index:
            current_image = self.image_list.get(selected_index[0])
            new_duration = self.duration_entry.get()
            try:
                self.image_data[current_image]["duration"] = int(new_duration)
            except ValueError:
                tk.messagebox.showerror("Error", "Please enter a valid integer for duration.")


if __name__ == "__main__":
    root = tk.Tk()
    app = LEDMatrixApp(root)
    root.mainloop()
