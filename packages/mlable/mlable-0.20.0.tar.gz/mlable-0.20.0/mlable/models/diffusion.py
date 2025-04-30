import functools

import tensorflow as tf

# import mlable.models
import mlable.shapes
import mlable.shaping.axes

import arcade.pipeline.diffusion
import arcade.plot

# CONSTANTS ####################################################################

START_RATE = 0.95 # signal rate at the start of the forward diffusion process
END_RATE = 0.02 # signal rate at the start of the forward diffusion process

# UTILITIES ####################################################################

def reduce_mean(data: tf.Tensor) -> tf.Tensor:
    return tf.math.reduce_mean(
        data,
        axis=tf.range(tf.rank(data) - 1),
        keepdims=True)

def reduce_std(data: tf.Tensor) -> tf.Tensor:
    return tf.math.reduce_std(
        data,
        axis=tf.range(tf.rank(data) - 1),
        keepdims=True)

# DIFFUSION WRAPPER ############################################################

@tf.keras.utils.register_keras_serializable(package='models')
class DiffusionModel(tf.keras.models.Model): # mlable.models.ContrastModel
    def __init__(
        self,
        start_rate: float=START_RATE, # signal rate at the start of the forward diffusion process
        end_rate: float=END_RATE, # signal rate at the start of the forward diffusion process
        **kwargs
    ) -> None:
        # init
        super(DiffusionModel, self).__init__(**kwargs)
        # save config for IO
        self._config = {'start_rate': start_rate, 'end_rate': end_rate,}
        # diffusion schedule
        self._schedule = functools.partial(arcade.pipeline.diffusion.cosine_rates, start_rate=start_rate, end_rate=end_rate)
        # scale the data to a normal distribution and back
        self._mean = tf.cast(0.0, dtype=tf.float32)
        self._std = tf.cast(1.0, dtype=tf.float32)
        # save the data shape for generation
        self._shape = ()

    def _norm(self, data: tf.Tensor, dtype: tf.DType=None) -> tf.Tensor:
        __dtype = dtype or self.compute_dtype
        return tf.cast((tf.cast(data, dtype=tf.float32) - self._mean) / self._std, dtype=__dtype)

    def _denorm(self, data: tf.Tensor, dtype: tf.DType=None) -> tf.Tensor:
        __dtype = dtype or self.compute_dtype
        return tf.cast(self._mean + self._std * tf.cast(data, dtype=tf.float32), dtype=__dtype)

    def adapt(self, dataset: tf.data.Dataset) -> None:
        __dtype = tf.float32
        # compute the dataset cardinality
        __scale = dataset.reduce(0, lambda __c, _: __c + 1)
        __scale = tf.cast(1.0, dtype=__dtype) / tf.cast(tf.maximum(1, __scale), dtype=__dtype)
        # compute the mean
        self._mean = __scale * dataset.reduce(0.0, lambda __m, __x: __m + reduce_mean(__x))
        self._mean = tf.cast(self._mean, dtype=__dtype)
        # compute the mean
        self._std = __scale * dataset.reduce(0.0, lambda __m, __x: __m + reduce_std(__x))
        self._std = tf.cast(self._std, dtype=__dtype)

    def build(self, input_shape: tuple) -> None:
        self._shape = tuple(input_shape[0])

    def postprocess(self, images: tf.Tensor) -> tf.Tensor:
        # scale the pixel values back to color space
        __images = self._denorm(images)
        # enforce min / max values
        __images = tf.clip_by_value(__images, 0.0, float(self._config['color_dim'] - 1))
        # enforce types
        return tf.cast(__images, dtype=tf.int32)

    def denoise(self, noisy_images: tf.Tensor, noise_rates: tf.Tensor, signal_rates: tf.Tensor) -> tuple:
        # predict noise component
        __noises = self.call((noisy_images, noise_rates**2), training=False)
        # remove noise component from data
        __images = (noisy_images - noise_rates * __noises) / signal_rates
        # return both
        return __noises, __images

    def reverse_diffusion(self, initial_noises: tf.Tensor, step_num: int) -> tf.Tensor:
        __dtype = self.compute_dtype
        # reverse diffusion = sampling
        __count = initial_noises.shape[0]
        __delta = 1.0 / step_num
        # the current predictions for the noise and the signal
        __noises = initial_noises
        __images = initial_noises
        for __i in range(step_num + 1):
            # even pure noise (step 0) is considered to contain some signal
            __angles = tf.ones((__count, 1, 1, 1), dtype=__dtype) - __i * __delta
            __alpha, __beta = self._schedule(__angles, dtype=__dtype)
            # remix the components, with a noise level corresponding to the current iteration
            __images = (__beta * __images + __alpha * __noises)
            # predict the cumulated noise in the image, and remove it from the image
            __noises, __images = self.denoise(__images, __alpha, __beta)
        return __images

    def generate(self, image_num: int, step_num: int) -> tf.Tensor:
        __dtype = self.compute_dtype
        __shape = (image_num,) + self._shape[1:]
        # sample the initial noise
        __noises = tf.random.normal(shape=__shape, dtype=__dtype)
        # remove the noise
        __images = self.reverse_diffusion(__noises, step_num)
        # denormalize
        return self.postprocess(__images)

    def train_step(self, data: tf.Tensor) -> dict:
        __dtype = self.compute_dtype
        __shape_n = tuple(data.shape)
        __shape_a = mlable.shapes.filter(data.shape, axes=[0])
        # normalize images to have standard deviation of 1, like the noises
        __images = self._norm(data)
        # sample the noises = targets
        __noises = tf.random.normal(shape=__shape_n, dtype=__dtype)
        # sample the diffusion angles
        __angles = tf.random.uniform(shape=__shape_a, minval=0.0, maxval=1.0, dtype=__dtype)
        # compute the signal to noise ratio
        __noise_rates, __signal_rates = self._schedule(__angles, dtype=__dtype)
        # mix the images with noises
        __images = __signal_rates * __images + __noise_rates * __noises
        # train to predict the noise from scrambled images
        return super(DiffusionModel, self).train_step(((__images, __noise_rates**2), __noises))

    def test_step(self, data: tf.Tensor) -> dict:
        __dtype = self.compute_dtype
        __shape_n = tuple(data.shape)
        __shape_a = mlable.shapes.filter(data.shape, axes=[0])
        # normalize images to have standard deviation of 1, like the noises
        __images = self._norm(data)
        # sample the noises = targets
        __noises = tf.random.normal(shape=__shape_n, dtype=__dtype)
        # sample the diffusion angles
        __angles = tf.random.uniform(shape=__shape_a, minval=0.0, maxval=1.0, dtype=__dtype)
        # compute the signal to noise ratio
        __noise_rates, __signal_rates = self._schedule(__angles, dtype=__dtype)
        # mix the images with noises
        __images = __signal_rates * __images + __noise_rates * __noises
        # train to predict the noise from scrambled images
        return super(DiffusionModel, self).test_step(((__images, __noise_rates**2), __noises))

    def plot_images(self, epoch: int=None, logs: dict=None, rows: int=2, cols: int=4, steps: int=16) -> None:
        # plot random generated images for visual evaluation of generation quality
        __images = tf.squeeze(self.generate(image_num=rows * cols, step_num=steps))
        # sort the images by (row, col)
        __images = mlable.shaping.axes.divide(__images, axis=0, factor=cols, insert=True, right=True)
        # actually plot
        with arcade.plot.PlotContext(rows=rows, cols=cols) as (_, __axes):
            for __i in range(rows):
                arcade.plot.sequence(__images[__i].numpy(), label='inputs', axes=__axes, stride=1, offset=[__i, 0], vertical=False)

    def get_config(self) -> dict:
        __config = super(DiffusionModel, self).get_config()
        __config.update(self._config)
        return __config

    @classmethod
    def from_config(cls, config: dict) -> tf.keras.layers.Layer:
        return cls(**config)
