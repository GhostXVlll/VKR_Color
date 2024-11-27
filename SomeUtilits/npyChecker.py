import numpy as np

# Замените 'путь_к_вашему_файлу' на реальный путь к вашему файлу NPY
data1 = np.load('E:/Study/Magister 2 course/Курсач/l/gray_scale.npy')
data2 = np.load('E:/Study/Magister 2 course/Курсач/ab/ab1.npy')

# Вывод первых пяти элементов массива
print("Первые пять элементов массива ЯРКОСТНЫХ КОМПОНЕНТ:")
print(data1[:5])
print("Первые пять элементов массива ЦВЕТОВЫХ КОМПОНЕНТ:")
print(data2[:5])