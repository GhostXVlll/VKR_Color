from PIL import Image
import os

# Указать путь к папке с изображениями
image_folder = 'E:/Study/Magister 2 course/Курсач/photos_black_white/'

# Пройтись по всем файлам в папке
for filename in os.listdir(image_folder):
    if filename.endswith('.jpg'):
        # Создать копию изображения
        image = Image.open(os.path.join(image_folder, filename))

        # Преобразовать изображение в чёрно-белое
        grayscale_image = image.convert('L')

        # Сохранить чёрно-белую копию
        new_filename = filename[:-4] + '_bw.jpg'
        grayscale_image.save(os.path.join(image_folder, new_filename))

print("Преобразование завершено.")