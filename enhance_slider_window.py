from tkinter import *


class EnhanceSliderWindow(Toplevel):
    def __init__(self, root, name, enhance, image, current_tab, update_method):
        super().__init__()
        self.name = name
        self.enhancer = enhance(image)
        self.original = image
        self.image = image.copy()
        self.current_tab = current_tab
        self.update_method = update_method

        self.init()

        self.factor = DoubleVar(value=1.0)

        self.scroll = Scale(
            self, label=self.name,
            from_=0.0, to=2.0, resolution=0.1, variable=self.factor,
            orient='horizontal', tickinterval=0.2,
            command=self.value_changed
        )
        self.apply = Button(self, text="Ок", command=self.close)
        self.cancel = Button(self, text="Отменить", command=self.cancel)

        self.draw_widgets()

    def init(self):
        self.title(f"Enhance{self.name}")
        self.geometry("320x120")
        self.iconbitmap("icon.ico")
        self.grab_focus()

    def grab_focus(self):
        self.grab_set()
        self.focus_force()

    def value_changed(self, value):
        self.image = self.enhancer.enhance(self.factor.get())
        self.update_method(self.current_tab, self.image)

    def draw_widgets(self):
        self.scroll.pack(fill="x", expand=1, pady=5, padx=5)
        self.apply.pack(side="left", expand=1, padx=5, pady=5)
        self.cancel.pack(side="right", expand=1, padx=5, pady=5)

    def cancel(self):
        self.update_method(self.current_tab, self.original)
        self.close()

    def close(self):
        self.destroy()
