import tkinter as tk
import threading
from yaml import safe_load
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

with open(BASE_DIR / "config" / "config.yml", "r") as file:
    config = safe_load(file)

ov = config["Overlay"]
size = ov["size"]
opacity = ov["opacity"]
position_x = ov["position_x"]
position_y = ov["position_y"]
color_idle = ov["color_idle"]
color_listening = ov["color_listening"]
color_thinking = ov["color_thinking"]
color_speaking = ov["color_speaking"]


class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_attributes("-toolwindow", True)
        self.root.title("Jarvis")
        self.root.geometry("{}x{}+{}+{}".format(
            size, size,
            self.root.winfo_screenwidth() - position_x,
            self.root.winfo_screenheight() - position_y
        ))
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", opacity)
        self.root.configure(bg="#010101")
        self.root.wm_attributes("-transparentcolor", "#010101")

        self.canvas = tk.Canvas(self.root, width=size, height=size, bg="#010101", highlightthickness=0)
        self.canvas.pack()

        # margines 8px z każdej strony
        margin = 8
        self.circle = self.canvas.create_oval(
            margin, margin,
            size - margin, size - margin,
            fill=color_idle, outline=""
        )

        self.root.protocol("WM_DELETE_WINDOW", self.hide)
        self._drag_x = 0
        self._drag_y = 0
        self.root.bind("<ButtonPress-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._drag)

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def _change_status(self, color: str):
        self.root.after(0, lambda: self.canvas.itemconfig(self.circle, fill=color))

    def set_idle(self):
        self._change_status(color_idle)

    def set_listening(self):
        self._change_status(color_listening)

    def set_speaking(self):
        self._change_status(color_speaking)

    def set_thinking(self):
        self._change_status(color_thinking)

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()

    def exit(self):
        self.root.destroy()

    def run(self):
        self.root.mainloop()