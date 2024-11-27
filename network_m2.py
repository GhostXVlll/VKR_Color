import tensorflow as tf
import keras
from keras import layers
from keras import ops


from keras_applications import Sequential
from keras.layers import Dense, Activation, Flatten
from keras.optimizers import Adam


#from tensorflow.keras.datasets import imagenet

import keras
print(tf.__version__)
print(keras.__version__)

(x_train, y_train), (x_test, y_test) = imagenet.load_data()

x_train = x_train.reshape((x_train.shape[0], 28, 28))
x_test = x_test.reshape((x_test.shape[0], 28, 28))

# Создание генератора
def generator(z):
    # Генератор создает цветные изображения
    model = Sequential()
    model.add(Dense(7 * 7 * 64, input_dim=100))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(14 * 14 * 3))
    model.add(Activation('sigmoid'))
    return model(z)

# Создание дискриминатора
def discriminator(image):
    # Дискриминатор оценивает реалистичность изображений
    model = Sequential()
    model.add(Dense(3 * 3 * 64, input_dim=784))
    model.add(Activation('relu'))
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(1))
    return model(image)

# Обучение GAN
gan = Sequential([generator, discriminator])
adam = Adam(learning_rate=0.001)
gan.compile(loss='binary_crossentropy', optimizer=adam)

# Тестирование GAN
for i in range(10):
    print("Iteration", i+1)
    gan.fit(x_train[:10], y_train[:10])

# Генерация цветных изображений
generated_images = gan.predict(x_test[:10])