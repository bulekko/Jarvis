import tkinter as tk
import logging
from PIL import Image, ImageDraw
from pystray import Icon, Menu, MenuItem
import threading


class Overlay:
    def __init__(self):
        self.root = tk.Tk()
        self.root.wm_attributes("-toolwindow", True)
        self.root.title("Jarvis")
        self.root.geometry("64x64+{}+{}".format(
            self.root.winfo_screenwidth() - 200,
            self.root.winfo_screenheight() - 200
        ))
        self.root.overrideredirect(True)
        self.root.configure(bg="#010101")
        self.root.wm_attributes("-transparentcolor", "#010101")

        self.canvas = tk.Canvas(self.root, width=64, height=64, bg="#010101", highlightthickness=0)
        self.canvas.pack()
        self.circle = self.canvas.create_oval(8, 8, 56, 56, fill="#626262", outline="")

        self.root.protocol("WM_DELETE_WINDOW", self.hide)
        self._drag_x = 0
        self._drag_y = 0
        self.root.bind("<ButtonPress-1>", self._start_drag)
        self.root.bind("<B1-Motion>", self._drag)

    def _change_status(self, color: str):
        self.root.after(0, lambda: self.canvas.itemconfig(self.circle, fill=color))

    def set_idle(self):
        self._change_status("#626262")

    def set_listening(self):
        self._change_status("#00C864")

    def set_speaking(self):
        self._change_status("#0096FF")

    def set_thinking(self):
        self._change_status("#FFB300")

    def _start_drag(self, event):
        self._drag_x = event.x
        self._drag_y = event.y

    def _drag(self, event):
        x = self.root.winfo_x() + event.x - self._drag_x
        y = self.root.winfo_y() + event.y - self._drag_y
        self.root.geometry(f"+{x}+{y}")

    def _update(self, status: str):
        self._change_status(status)
        threading.Thread(target=self._change_status, args=(status), daemon=True).start()

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()

    def exit(self):
        self.tray.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()