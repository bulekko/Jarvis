import customtkinter as ctk
import pystray
from PIL import Image, ImageDraw
import threading

ctk.set_appearance_mode("dark")


class Overlay:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.wm_attributes("-toolwindow", True)
        self.root.title("Jarvis")
        self.root.geometry("300x90+{}+{}".format(
            self.root.winfo_screenwidth() - 350,
            self.root.winfo_screenheight() - 170
        ))
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)

        self.status_label = ctk.CTkLabel(
            self.root,
            text="Sleeping...",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="gray"
        )
        self.status_label.pack(expand=True)

        self.text_label = ctk.CTkLabel(
            self.root,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.text_label.pack(expand=True)

        # tray icon
        self.tray = None
        threading.Thread(target=self._setup_tray, daemon=True).start()

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

    def _setup_tray(self):
        image = Image.new("RGB", (64, 64), color=(30, 30, 30))
        draw = ImageDraw.Draw(image)
        draw.ellipse([16, 16, 48, 48], fill=(0, 200, 100))

        self.tray = pystray.Icon(
            "Jarvis",
            image,
            "Jarvis",
            menu=pystray.Menu(
                pystray.MenuItem("Show", self.show),
                pystray.MenuItem("Exit", self.exit)
            )
        )
        self.tray.run()

    def set_idle(self):
        self.root.after(0, lambda: self._update("Sleeping...", "", "gray"))

    def set_listening(self):
        self.root.after(0, lambda: self._update("Listening...", "", "#00C864"))

    def set_speaking(self, text: str = ""):
        self.root.after(0, lambda: self._update("Speaking...", text, "#0096FF"))

    def set_thinking(self):
        self.root.after(0, lambda: self._update("Thinking...", "", "#FFB300"))

    def _update(self, status: str, text: str, color: str):
        self.status_label.configure(text=status, text_color=color)
        self.text_label.configure(text=text, text_color=color)
        self.status_label.place(relx=0.5, rely=0.3, anchor="center")
        self.text_label.place(relx=0.5, rely=0.7, anchor="center")
        self.root.configure(fg_color="#1a1a1a")

    def hide(self):
        self.root.withdraw()

    def show(self):
        self.root.deiconify()

    def exit(self):
        self.tray.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()