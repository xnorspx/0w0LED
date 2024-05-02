import serial.tools.list_ports
import serial
from tkinter import Tk, filedialog
import time
import os
import rich.console

# Get config file path
root = Tk()
animation_path = filedialog.askopenfilename(title="Animation", initialdir=os.getcwd())
root.destroy()

# Parse profile
with open(animation_path, "r", encoding="utf-8") as f:
    raw_images = f.read()
raw_images = raw_images.split("\n")

duration = 0
images = []
for item in raw_images:
    if item:
        item = item.split(",")
        images.append(
            (item[1], item[2].upper() + ";;")
        )
        duration += int(item[1])

# Tool func
start_time = time.time() * 1000


def current_image() -> str:
    cur_time = time.time() * 1000
    delta_time = (cur_time - start_time) % duration
    index = 0
    while delta_time > 0:
        delta_time -= float(images[index][0])
        index += 1
    return images[index - 1][1]


# Initiate serial connection
terminal = rich.console.Console()

avail_serial_ports = serial.tools.list_ports.comports()
if len(avail_serial_ports) == 1:
    serial_port = avail_serial_ports[0].name
else:
    # Ask for the desired serial port
    terminal.print("The following are the available serial ports:", style="cyan")
    for item in avail_serial_ports:
        terminal.print(item.name, style="green")
    terminal.print("Please input the serial port that you want to use: ", style="yellow", end="")
    serial_port = terminal.input()

serial_obj = serial.Serial(serial_port, baudrate=2000000)
terminal.clear()

# Main loop
while True:
    cmd = serial_obj.readline().strip()
    terminal.print(f"{time.time() * 1000 - start_time} <- {cmd}", style="green")
    if cmd == b"Poll":
        image_bit = f"{current_image()}\n".encode("ascii")
        # terminal.print(f"{time.time() * 1000 - start_time} -> {image_bit}", style="green")
        serial_obj.write(image_bit)
