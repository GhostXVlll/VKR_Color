import tensorflow as tf
import tensorflow
import tensorflow.keras

def build_encoder(input_shape):
    inputs = keras.Input(shape=input_shape)
    x = layers.Conv2D(32, 3, strides=2, padding="same")(inputs)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Conv2D(64, 3, strides=2, padding="same")(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Conv2D(128, 3, strides=2, padding="same")(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Flatten()(x)
    x = layers.Dense(1024)(x)
    x = layers.LeakyReLU(alpha=0.2)(x)

    mean = layers.Dense(latent_dim, name="mean")(x)
    log_var = layers.Dense(latent_dim, name="log_var")(x)

    encoder = keras.Model(inputs, [mean, log_var], name="encoder")
    return encoder

def build_decoder(latent_dim):
    latent_inputs = keras.Input(shape=(latent_dim,))
    x = layers.Dense(7 * 7 * 128)(latent_inputs)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Reshape((7, 7, 128))(x)
    x = layers.Conv2DTranspose(128, 3, strides=2, padding="same")(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Conv2DTranspose(64, 3, strides=2, padding="same")(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Conv2DTranspose(32, 3, strides=1, padding="same")(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    outputs = layers.Conv2D(2, 3, padding="same")(x)  # 2 channels for colorization (R, G)

    decoder = keras.Model(latent_inputs, outputs, name="decoder")
    return decoder

def sampling(args):
    mean, log_var = args
    epsilon = tf.random.normal(shape=tf.shape(mean))
    return mean + tf.exp(0.5 * log_var) * epsilon

def vae_loss(x, x_decoded):
    reconstruction_loss = tf.reduce_mean(keras.losses.mse(x, x_decoded))
    kl_loss = -0.5 * tf.reduce_mean(1 + log_var - tf.square(mean) - tf.exp(log_var))
    return reconstruction_loss + kl_loss

latent_dim = 16
input_shape = (28, 28, 1)  # Example input shape for MNIST-like images

encoder = build_encoder(input_shape)
decoder = build_decoder(latent_dim)

inputs = keras.Input(shape=input_shape)
mean, log_var = encoder(inputs)
z = layers.Lambda(sampling)([mean, log_var])
outputs = decoder(z)

vae = keras.Model(inputs, outputs)
vae.compile(optimizer="adam", loss=vae_loss)
