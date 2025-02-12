"""
CerranetV3 - Deep Learning Model for Classification
Software Open Source
Copyright © Mateus de Souza Miranda, 2023
Contact: mateus.miranda@inpe.br; mateusmirandaa2@hotmail.com
National Institute for Space Research (INPE)
São José dos Campos, São Paulo, Brazil

Version 4: January 2023
"""

import tensorflow as tf
from tensorflow.keras import layers, models, Sequential


class CerranetV3:
    """CerranetV3 model for image classification.

    Args:
        image_size (int): Input image dimensions (assumes square images)
        num_classes (int): Number of output classes
        channels (int): Number of input channels (default: 3)
        act_layer (str): Activation function for output layer (default: 'softmax')
    """

    def __init__(self,
                 image_size: int,
                 num_classes: int,
                 channels: int = 3,
                 act_layer: str = 'softmax',
                 loss_func: str = 'categorical_crossentropy'):
        self.image_size = image_size
        self.num_classes = num_classes
        self.channels = channels
        self.act_layer = act_layer
        self.loss_func = loss_func

    def build_model(self) -> tf.keras.Model:
        """Construct and compile the CNN model.

        Returns:
            tf.keras.Model: Compiled Keras model
        """
        model = Sequential()

        # Input Layer with configurable channels
        model.add(layers.Input(shape=(self.image_size, self.image_size, self.channels)))

        # Convolutional Blocks
        for filters in [64, 64, 128, 128, 256, 256]:
            model.add(layers.Conv2D(filters, (3, 3), activation='relu'))
            model.add(layers.AveragePooling2D(pool_size=(2, 2)))
            model.add(layers.Dropout(0.15))

        # Classification Head
        model.add(layers.Flatten())
        model.add(layers.Dense(256, activation='relu'))
        model.add(layers.Dropout(0.15))
        model.add(layers.Dense(128, activation='relu'))
        model.add(layers.Dropout(0.1))
        model.add(layers.Dense(self.num_classes, activation=self.act_layer))

        # Compile model
        model.compile(
            optimizer='adam',
            loss=self.loss_func,
            metrics=['accuracy']
        )

        return model

