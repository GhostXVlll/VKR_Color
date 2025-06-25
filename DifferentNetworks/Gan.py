import numpy as np
import skimage.transform as t
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.optimizers as optimizers
from PIL.Image import Image
from keras.src.layers import Activation
import matplotlib.pyplot as plt

# Загрузка данных
L = np.load('l/gray_scale.npy')
ab1 = np.load('ab/ab1.npy')
ab2 = np.load('ab/ab2.npy')
ab3 = np.load('ab/ab3.npy')
AB = np.concatenate((ab1, ab2, ab3), axis=0)

print(L.shape)
print(AB.shape)

# Создание генератора
def build_generator(input_dim):
    model = models.Sequential()
    model.add(layers.Input(shape=(input_dim,)))
    # Входной слой
    model.add(layers.Dense(128, activation='relu'))
    # Скрытые слои
    model.add(layers.Dense(64, activation='sigmoid'))
    return model

# Создание дискриминатора
def build_discriminator():
    model = models.Sequential()
    model.add(layers.Input(shape=(224, 224, 1)))  # Исправлено на (224, 224, 1)
    # Скрытые слои
    model.add(layers.Flatten())  # Добавление Flatten слоя для преобразования в 1D
    model.add(layers.Dense(32, activation='leaky_relu'))
    model.add(layers.Dense(224 * 224 * 2, activation='leaky_relu'))  # Изменено на 224 * 224 * 2
    model.add(layers.Reshape((224, 224, 2)))  # Изменено на (224, 224, 2)
    # Выходное значение
    model.add(Activation('sigmoid'))
    return model

# Компиляция модели
generator = build_generator(input_dim=10)
discriminator = build_discriminator()

optimizer = optimizers.Adam(learning_rate=0.001)
discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Обучение модели
history = discriminator.fit(L, AB, epochs=2, batch_size=32)

# Использование модели для раскраски
L_new = np.array([[127, 131, 159],
                  [113, 128, 160],
                  [ 95,  86,  96]])
L_new = L_new.reshape(1, 3, 3, 1)  # Добавляем размерность для канала
L_new = t.resize(L_new, (1, 224, 224, 1))  # Изменяем размер на (1, 224, 224, 1)
AB_pred = discriminator.predict(L_new)
A_pred = AB_pred[:, :, :, 0]
B_pred = AB_pred[:, :, :, 1]
print(A_pred)
print(B_pred)

lab_image = np.dstack((L_new, AB_pred))

plt.imshow(lab_image)
