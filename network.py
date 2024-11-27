import numpy as np
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.src.layers import Conv2D, InputLayer
#from skimage.color import lab2rgb, rgb2lab
import os.path

#from tensorflow.keras.preprocessing.image import img_to_array, load_img
from PIL import Image, ImageOps

# Defaults
path = 'E:/Study(4 Course)/4 course/ВКР/Colorize_v3/Colorize/Lib/'
learningPath = path + 'Images/LearningSelection/'
# -------------------------------------------------------


def load(modelName):
    try:  # Пробуем подгрузить существующую модель
        print("Trying to load model..")
        model = load_model(modelName)
        print('Model ' + str(model) + ' was loaded.')
        return model
    except:  # Если не вышло, обучаем и сохраняем модель
        create_model(modelName)
        return model


def create_model(modelName):
    print('Learning started...')
    X = []
    for filename in os.listdir(learningPath):
        X.append(img_to_array(load_img(learningPath + filename)))
    X = np.array(X, dtype=float)

    split = int(0.95 * len(X))
    Xtrain = X[:split]
    Xtrain = 1.0 / 255 * Xtrain

    model = Sequential()
    model.add(InputLayer(input_shape=(None, None, 1)))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same', strides=2))
    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(256, (3, 3), activation='relu', padding='same', strides=2))
    model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
    from tensorflow.python.keras.layers import UpSampling2D
    model.add(UpSampling2D((2, 2,)))
    model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
    model.add(UpSampling2D((2, 2,)))
    model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
    model.add(UpSampling2D((2, 2,)))

    model.compile(optimizer='adam', loss='mse')

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(shear_range=0.2, zoom_range=0.2, rotation_range=20,
                                                              horizontal_flip=True)

    batch_size = 10

    def image_a_b_gen(batch_size):
        for batch in datagen.flow(Xtrain, batch_size=batch_size):
            lab_batch = rgb2lab(batch)
            X_batch = lab_batch[:, :, :, 0]
            Y_batch = lab_batch[:, :, :, 1:] / 128
            yield X_batch.reshape(X_batch.shape + (1,)), Y_batch

    model.fit(image_a_b_gen(batch_size), steps_per_epoch=100, epochs=100)

    Xtest = rgb2lab(1.0 / 255 * X[split:])[:, :, :, 0]
    Xtest = Xtest.reshape(Xtest.shape + (1,))
    Ytest = rgb2lab(1.0 / 255 * X[split:])[:, :, :, 1:]
    Ytest = Ytest / 128

    print(model.evaluate(Xtest, Ytest, batch_size=batch_size))
    model.save('E:/Study(4 Course)/4 course/ВКР/Colorize_v3/Colorize/Lib/models/' + modelName)


def prediction(image, model='E:/Study(4 Course)/4 course/ВКР/Colorize_v3/Colorize/Lib/models/++4_50epochs_100steps.h5'):
    img = image
    # подготовка
    width, height = img.size  # сохраним исходные размеры изображения
    temp = img.resize((256, 256), Image.BILINEAR)

    temp = np.array(temp, dtype=float)
    size = temp.shape

    lab = rgb2lab(1.0/255 * temp)
    X, Y = lab[:, :, 0], lab[:, :, 1:]

    Y = Y / 128  # нормируем выходное значение в диапазон от -1 до 1
    X = X.reshape(1, size[0], size[1], 1)
    Y = Y.reshape(1, size[0], size[1], 2)

    output = model.predict(X)

    output *= 128
    min_vals, max_vals = -128, 127
    ab = np.clip(output[0], min_vals, max_vals)

    cur = np.zeros((size[0], size[1], 3))
    cur[:, :, 0] = np.clip(X[0][:, :, 0], 0, 100)
    cur[:, :, 1:] = ab
    cur = (lab2rgb(cur))
    # Возвращаем изображению первоначальную форму
    output = Image.fromarray((cur * 255).astype(np.uint8))
    # увеличение изображения до масштаба 3000х3000 пикселей
    output = ImageOps.contain(output, (3000, 3000), method=Image.LANCZOS)
    # возврат пропорций
    output = output.resize((width, height), Image.BILINEAR)
    return output