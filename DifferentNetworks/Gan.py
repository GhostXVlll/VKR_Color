import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

# Загрузка данных
L = np.load('l.npy')
AB = np.load('ab.npy')

# Создание генератора
def generator(z):
    # Входной слой
    x = Dense(128, activation='relu')(z)
    # Скрытые слои
    x = Dense(64, activation='sigmoid')(x)
    # Выходной слой
    return x

# Создание дискриминатора
def discriminator(x):
    # Входное изображение
    x = Flatten()(x)
    # Скрытые слои
    x = Dense(32, activation='leaky_relu')(x)
    x = Dense(16, activation='leaky_relu')(x)
    # Выходное значение
    return Activation('sigmoid')(x)

# Компиляция модели
model = Sequential()
model.add(generator(np.zeros((10, 1))))
model.add(discriminator)
optimizer = Adam(learning_rate=0.001)
model.compile(loss='binary_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# Обучение модели
history = model.fit(L, AB, epochs=100, batch_size=32)

# Использование модели для раскраски
L_new = np.array([[127, 131, 159],
                  [113, 128, 160],
                  [ 95,  86,  96]])
A_pred, B_pred = model.predict(L_new)
print(A_pred)
print(B_pred)