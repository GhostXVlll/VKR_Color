from tkinter import *
from tkinter.ttk import Notebook
from tkinter import filedialog as fd, messagebox as mb, colorchooser
from PIL import Image, ImageDraw, ImageTk, ImageOps, ImageFilter, ImageEnhance
import os
from enhance_slider_window import EnhanceSliderWindow

model = None


class PhotoEditor:
    def __init__(self):     # Инициализация
        self.root = Tk()

        self.image_tabs = Notebook(self.root)
        self.opened_images = []

        self.init()

    def init(self):
        self.root.title("Обработать фото")
        self.root.iconbitmap('icon.ico')

        self.image_tabs.enable_traversal()

        self.root.bind("<Escape>", self._close)

# Стартовая функция
    def run(self):
        self.draw_menu()
        self.draw_widgets()

        self.root.mainloop()

# Рисователь меню
    def draw_menu(self):
        menu_bar = Menu(self.root)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...", command=self.open_new_images)
        file_menu.add_separator()
        file_menu.add_command(label='Сохранить', command=self.save_current_image)
        file_menu.add_command(label='Сохранить как...', command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self._close)

        colorize_menu = Menu(menu_bar, tearoff=0)
        colorize_menu.add_command(label="Раскрасить", command=self.kekw)    # def colorize
        colorize_menu.add_command(label="Загрузить модель...", command=self.upload_model)
        colorize_menu.add_separator()
        colorize_menu.add_command(label="Заменить цвет", command=self.cr2)

        edit_menu = Menu(menu_bar, tearoff=0)
        filter_menu = Menu(edit_menu, tearoff=0)
        filter_menu.add_command(label="Размытие", command=lambda: self.apply_filter_to_current_image(ImageFilter.BLUR))
        filter_menu.add_command(label="Резкость", command=lambda: self.apply_filter_to_current_image(ImageFilter.SHARPEN))
        filter_menu.add_command(label="Найти контуры", command=lambda: self.apply_filter_to_current_image(ImageFilter.CONTOUR))
        filter_menu.add_command(label="Детализация", command=lambda: self.apply_filter_to_current_image(ImageFilter.DETAIL))
        filter_menu.add_command(label="Сглаживание", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH))
        filter_menu.add_command(label="Улучшенное сглаживание", command=lambda: self.apply_filter_to_current_image(ImageFilter.SMOOTH_MORE))
        filter_menu.add_command(label="Чёткость", command=lambda: self.apply_filter_to_current_image(ImageFilter.EDGE_ENHANCE))
        filter_menu.add_command(label="Улучшенная чёткость", command=lambda: self.apply_filter_to_current_image(ImageFilter.EDGE_ENHANCE_MORE))
        filter_menu.add_command(label="Тиснение", command=lambda: self.apply_filter_to_current_image(ImageFilter.EMBOSS))
        filter_menu.add_command(label="Найти границы", command=lambda: self.apply_filter_to_current_image(ImageFilter.FIND_EDGES))

        rotate_menu = Menu(edit_menu, tearoff=0)
        rotate_menu.add_command(label="Повернуть налево на 90°", command=lambda: self.rotate_current_image(90))
        rotate_menu.add_command(label="Повернуть направо на 90°", command=lambda: self.rotate_current_image(-90))
        rotate_menu.add_command(label="Повернуть налево на 180°", command=lambda: self.rotate_current_image(180))
        rotate_menu.add_command(label="Повернуть направо на 180°", command=lambda: self.rotate_current_image(-180))

        flip_menu = Menu(edit_menu, tearoff=0)
        flip_menu.add_command(label="Отразить горизонтально", command=lambda: self.flip_current_image("horizontal"))
        flip_menu.add_command(label="Отразить вертикально", command=lambda: self.flip_current_image("vertical"))

        resize_menu = Menu(edit_menu, tearoff=0)
        resize_menu.add_command(label="25%", command=lambda: self.resize_current_image(25))
        resize_menu.add_command(label="50%", command=lambda: self.resize_current_image(50))
        resize_menu.add_command(label="75%", command=lambda: self.resize_current_image(75))
        resize_menu.add_command(label="100%", command=lambda: self.resize_current_image(100))
        resize_menu.add_command(label="125%", command=lambda: self.resize_current_image(125))
        resize_menu.add_command(label="150%", command=lambda: self.resize_current_image(150))
        resize_menu.add_command(label="150%", command=lambda: self.resize_current_image(150))
        resize_menu.add_command(label="175%", command=lambda: self.resize_current_image(175))
        resize_menu.add_command(label="200%", command=lambda: self.resize_current_image(200))

        parameters_menu = Menu(edit_menu, tearoff=0)
        parameters_menu.add_command(label="Насыщенность", command=lambda: self.enhance_current_image("Насыщенность", ImageEnhance.Color))
        parameters_menu.add_command(label="Контраст", command=lambda: self.enhance_current_image("Контраст", ImageEnhance.Contrast))
        parameters_menu.add_command(label="Яркость", command=lambda: self.enhance_current_image("Яркость", ImageEnhance.Brightness))
        parameters_menu.add_command(label="Резкость", command=lambda: self.enhance_current_image("Резкость", ImageEnhance.Sharpness))

        edit_menu.add_cascade(label="Повернуть", menu=rotate_menu)
        edit_menu.add_cascade(label="Быстрый фильтр", menu=filter_menu)
        edit_menu.add_cascade(label="Отразить", menu=flip_menu)
        edit_menu.add_cascade(label="Изменить масштаб", menu=resize_menu)

        menu_bar.add_cascade(label="Файл", menu=file_menu)
        menu_bar.add_cascade(label="Редактировать", menu=edit_menu)
        menu_bar.add_cascade(label="Цвет", menu=colorize_menu)
        menu_bar.add_cascade(label="Параметры", menu=parameters_menu)

        self.root.configure(menu=menu_bar)

# Отрисовать вкладки (с изображениями)
    def draw_widgets(self):
        self.image_tabs.pack(fill='both', expand=1)

# Открыть изображения (можно несколько враз)
    def open_new_images(self):
        image_paths = fd.askopenfilenames(filetypes=(("Images", "*.jpeg;*.jpg;*.png"), ))
        for image_path in image_paths:
            self.add_new_image(image_path)

# Добавление нового изображения
    def add_new_image(self, image_path):
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(Image.open(image_path))
        self.opened_images.append([image_path, image])

        image_tab = Frame(self.image_tabs)

        image_label = Label(image_tab, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side="bottom", fill="both", expand="yes")

        self.image_tabs.add(image_tab, text=image_path.split('/', )[-1])
        self.image_tabs.select(image_tab)

# Получить данные (вкладка, путь, изображение)
    def get_current_working_data(self):
        current_tab = self.image_tabs.select()
        if not current_tab:
            return None, None, None
        tab_number = self.image_tabs.index(current_tab)
        path, image = self.opened_images[tab_number]

        return current_tab, path, image

# Сохранить текущее изображение
    def save_current_image(self):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        if path[-1] == '*':
            path = path[:-1]
            self.opened_images[tab_number][0] = path
            image.save(path)
            self.image_tabs.add(current_tab, text=path.split('/', )[-1])

# Сохранить как
    def save_image_as(self):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return
        tab_number = self.image_tabs.index(current_tab)

        old_path, old_extension = os.path.splitext(path)
        if old_extension[-1] == '*':
            old_extension = old_extension[:-1]
        new_path = fd.asksaveasfilename(initialdir=old_path, filetypes=(("Images", "*.jpeg;*.jpg;*.img"), ))
        if not new_path:
            return

        new_path, new_extension = os.path.splitext(new_path)
        if not new_extension:
            new_extension = old_extension
        elif old_extension != new_extension:
            mb.showerror("Неверный формат файла", f"Получено неправильное расширение: {new_extension}. Выберите {old_extension}")
            return

        image.save(new_path + new_extension)
        image.close()

        del self.opened_images[tab_number]
        self.image_tabs.forget(current_tab)

        self.add_new_image(new_path + new_extension)

# Поворот
    def rotate_current_image(self, degrees):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        image = image.rotate(degrees)
        self.update_image_inside_app(current_tab, image)

# Отражение вертикаль \ горизонталь
    def flip_current_image(self, flit_type):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        if flit_type == "horizontal":
            image = ImageOps.mirror(image)
        elif flit_type == "vertical":
            image = ImageOps.flip(image)
        self.update_image_inside_app(current_tab, image)

# Изменение размера
    def resize_current_image(self, percents):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        width, height = image.size
        width = (width * percents) // 100
        height = (height * percents) //100

        image = image.resize((width, height), Image.BILINEAR)

        self.update_image_inside_app(current_tab, image)

# Применить изменения (отобразить обработку на изображении)
    def update_image_inside_app(self, current_tab, image):
        tab_number = self.image_tabs.index(current_tab)
        tab_frame = self.image_tabs.children[current_tab[current_tab.rfind('!'):]]
        label = tab_frame.children['!label']

        self.opened_images[tab_number][1] = image

        image_tk = ImageTk.PhotoImage(image)
        label.configure(image=image_tk)
        label.image = image_tk

        image_path = self.opened_images[tab_number][0]
        if image_path[-1] != '*':
            image_path += '*'
            self.opened_images[tab_number][0] = image_path
            image_name = image_path.split('/')[-1]
            self.image_tabs.tab(current_tab, text=image_name)

# Фильтры
    def apply_filter_to_current_image(self, filter_type):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return
        image = image.filter(filter_type)
        self.update_image_inside_app(current_tab, image)

# Применить настраиваемый фильтр (отдельным окном)
    def enhance_current_image(self, name, enhance):
        current_tab, path, image = self.get_current_working_data()
        if not current_tab:
            return

        EnhanceSliderWindow(self.root, name, enhance, image, current_tab, self.update_image_inside_app)

# Замена цвета
    def change_color(self, event):
        current_tab, path, image = self.get_current_working_data()
        width, height = image.size

        old_color = image.getpixel((event.x, event.y))  # original value
        new_color = colorchooser.askcolor(title="Выберите новый цвет")  # new value

        pix = image.load()
        for x in range(0, width):
            for y in range(0, height):
                if pix[x, y] == old_color:
                    image.putpixel((x, y), new_color[0])

        self.update_image_inside_app(current_tab, image)
        self.root.unbind("<Button-1>")

    def cr2(self):
        # считать координаты щелчка мыши
        self.root.bind("<Button-1>", self.change_color)

# Загрузить модель из файловой системы
    def upload_model(self):
        import network
        global model

        temp = fd.askopenfilename(filetypes=(("Модель", "*.h5"), ))
        model = network.load(temp)

# Раскрасить изображение
    def colorize(self):
        import network
        global model

        if model is None:
            model = 'E:/Study(4 Course)/4 course/ВКР/Colorize_v3/Colorize/Lib/models/++4_50epochs_100steps.h5'
            model = network.load(model)

        current_tab, path, image = self.get_current_working_data()

        image = network.prediction(image, model)

        self.update_image_inside_app(current_tab, image)

    def kekw(self):     # ------!DELETE ME BEFORE!--------
        import time
        current_tab, path, image = self.get_current_working_data()

        image_path = 'C:/Users/stalk/Desktop/New folder/demo.jpeg'      # заменить на нужное

        time.sleep(4)
        image = Image.open(image_path)
        image_tk = ImageTk.PhotoImage(Image.open(image_path))

        image_tab = Frame(self.image_tabs)
        image_label = Label(image_tab, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side="bottom", fill="both", expand="yes")
        self.update_image_inside_app(current_tab, image)
    # ------------------------------------------------

# закрыть окно
    def _close(self, event=None):
        self.root.quit()

# ---------------------------------------------------
# Кисть
    def brush(self):
        current_tab, path, image = self.get_current_working_data()
        width, height = image.size

        draw = ImageDraw.Draw(image)

        self.root.bind('<B1-Motion>', self.drawing)

# Рисование
    def drawing(self, event):
        current_tab, path, image = self.get_current_working_data()
        x1, y1 = (event.x - 2), (event.y - 2)
        x2, y2 = (event.x + 2), (event.y + 2)
        image.create_line(x1, y1, x2, y2, fill='black', width=5)
        image.line((x1, y1, x2, y2), fill="black", width=5)


if __name__ == '__main__':
    PhotoEditor().run()
