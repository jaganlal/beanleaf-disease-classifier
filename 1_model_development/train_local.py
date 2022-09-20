import os

import argparse
import logging
from time import process_time_ns

import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_hub as hub

import numpy as np

import warnings
warnings.filterwarnings('ignore')

import re

class BeanleafDiseaseClassifier():
    def __init__(self, args):
        self.args = args

    def create_pipeline(self):
        batch_size = 128
        img_height = 224
        img_width = 224

        # DATA needs to be ready here
        beanleaf_dataset_train_path = os.path.join(self.args.container_name, 'train')
        beanleaf_dataset_test_path = os.path.join(self.args.container_name, 'test')
        beanleaf_dataset_validation_path = os.path.join(self.args.container_name, 'validation')

        train_ds = tf.keras.preprocessing.image_dataset_from_directory(beanleaf_dataset_train_path, seed=111, image_size=(img_height, img_width), batch_size=batch_size)
        test_ds = tf.keras.preprocessing.image_dataset_from_directory(beanleaf_dataset_test_path, seed=111, image_size=(img_height, img_width), batch_size=batch_size)
        val_ds = tf.keras.preprocessing.image_dataset_from_directory(beanleaf_dataset_validation_path, seed=111, image_size=(img_height, img_width), batch_size=batch_size)

        for image_batch, labels_batch in train_ds:
            print(image_batch.shape)
            print(labels_batch.shape)
            break

        classes = train_ds.class_names
        print(classes)

        AUTOTUNE = tf.data.AUTOTUNE
        train_ds = train_ds.cache().prefetch(buffer_size = AUTOTUNE)
        val_ds = val_ds.cache().prefetch(buffer_size = AUTOTUNE)

        feature_extractor = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
        feature_extractor_layer = hub.KerasLayer(feature_extractor, input_shape = (img_height,img_width, 3))
        feature_extractor_layer.trainable = False

        normalization_layer = tf.keras.layers.experimental.preprocessing.Rescaling(1./255)
        tf.random.set_seed(111)

        model = tf.keras.Sequential([
                        normalization_layer,
                        feature_extractor_layer,
                        tf.keras.layers.Dropout(0.3),
                        tf.keras.layers.Dense(3,activation='softmax')
        ])

        model.compile(
                        optimizer='adam',
                        loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
                        metrics=['accuracy']
        )

        model.fit(train_ds, epochs = 1, validation_data = val_ds)

        # joblib.dump(model, self.args.model_path)
        model.save(self.args.model_path, save_format='tf')

        test_loss, test_acc = model.evaluate(test_ds)
        print('Test Accuracy:', test_acc)
        print('Test Loss:', test_loss)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QA Code Indexing pipeline')
    parser.add_argument('--container_name', type=str, help='Path to default datastore container', default='beanleaf_dataset')
    parser.add_argument('--dataset_name', type=str, help='Dataset name to store in workspace', default='beanleaf')
    parser.add_argument('--dataset_desc', type=str, help='Dataset description', default='')
    parser.add_argument('--model_path', type=str, help='Path to store the model', default='./local_training/models')
    parser.add_argument('--artifact_loc', type=str, 
                        help='DevOps artifact location to store the model', default='./outputs/models/')
    args = parser.parse_args()
    beanleaf_disease_classifier = BeanleafDiseaseClassifier(args)
    beanleaf_disease_classifier.create_pipeline()