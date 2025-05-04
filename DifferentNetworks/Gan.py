import numpy as np
import tensorflow.keras.models as models
import tensorflow.keras.layers as layers
import tensorflow.keras.optimizers as optimizers
from keras.src.layers import Activation

# Загрузка данных
L = np.load('l/gray_scale.npy')
ab1 = np.load('ab/ab1.npy')
ab2 = np.load('ab/ab2.npy')
ab3 = np.load('ab/ab3.npy')
AB = np.concatenate((ab1,ab2,ab3), axis=0)

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
    model.add(layers.Input(shape=(256,)))  # Пример формы входных данных
    # Скрытые слои
    model.add(layers.Dense(32, activation='leaky_relu'))
    model.add(layers.Dense(16, activation='leaky_relu'))
    # Выходное значение
    model.add(Activation('sigmoid'))
    return model

# Компиляция модели
generator = build_generator(input_dim=10)  # Пример размерности входных данных
discriminator = build_discriminator()

optimizer = optimizers.Adam(learning_rate=0.001)
discriminator.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Обучение модели
history = discriminator.fit(L, AB, epochs=100, batch_size=32)

# Использование модели для раскраски
L_new = np.array([[127, 131, 159],
                  [113, 128, 160],
                  [ 95,  86,  96]])
A_pred, B_pred = discriminator.predict(L_new)
print(A_pred)
print(B_pred)
