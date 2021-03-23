# -*- coding: utf-8 -*-
# DenseNet121.py
'''
Implementation of the DenseNet121 architecture.
Structure: INPUT --> ...
'''
import tensorflow as tf
import config
from tensorflow.keras import layers

class DenseNet121:
    '''
    DenseNet121 Architecture implemented using tf.keras.applications
    '''

    @staticmethod
    def build(num_classes:int):
        
        '''
        Build the DenseNet121 architecture given the corresponding
        number of classes of the data.
        
        parameters
        ----------
            num_classes: number of classes of the corresponding data.

        returns
        -------
            model: the DenseNet121 model compatible with given inputs
        '''
        # initialize model
        print("[INFO] preparing model...")

        # Create a model that includes the augmentation stage
        input_shape=(config.img_height, config.img_width, config.depth)
        
        inputs = tf.keras.Input(shape=input_shape)

        # augment images
        data_augmentation = tf.keras.Sequential(
        [
        layers.experimental.preprocessing.RandomFlip("horizontal", input_shape=(config.img_height, config.img_width, config.depth)),
        layers.experimental.preprocessing.RandomRotation(0.1),
        layers.experimental.preprocessing.RandomZoom(0.1),
        layers.experimental.preprocessing.Rescaling(1./127.5, offset= -1)
        ]
        )
                
        x = data_augmentation(inputs)
        #preprocess_input = tf.keras.applications.DenseNet121.preprocess_input

        # load the DenseNet121 network, ensuring the head FC layer sets are left off
        baseModel = tf.keras.applications.DenseNet121(include_top=False, weights=config.weights, input_shape=input_shape)
        baseModel.trainable = config.trainable
        #baseModel.summary()
             
        # construct the head of the model that will be placed on top of the the base model
        headModel = baseModel.output

        headModel = tf.keras.layers.GlobalAveragePooling2D()(headModel)
        '''
        headModel = tf.keras.layers.AveragePooling2D(pool_size=(6, 6))(headModel)
        headModel = tf.keras.layers.Flatten(name="flatten")(headModel)
        headModel = tf.keras.layers.Dense(256, activation="relu")(headModel)
        '''
        
        headModel = tf.keras.layers.Dropout(0.2)(headModel)
        headModel = tf.keras.layers.Dense(num_classes, activation="softmax")(headModel)
        # place the head FC model on top of the base model (this will become
        # the actual model we will train)
        model = tf.keras.Model(inputs=baseModel.input, outputs=headModel)

        return model