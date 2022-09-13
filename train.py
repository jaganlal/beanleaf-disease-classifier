import os

from azureml.core import Datastore, Dataset
from azureml.core.run import Run
import argparse
import logging

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
        self.run = Run.get_context()
        self.workspace = self.run.experiment.workspace

    def create_pipeline(self):
        batch_size = 128
        img_height = 224
        img_width = 224

        datastore_paths = [(self.datastore, os.path.join(self.args.container_name, 'train'))]
        # data_ds = Dataset.Tabular.from_delimited_files(path=datastore_paths)
        train_data_ds = Dataset.File.from_files(path=datastore_paths)
        dataset_name = self.args.dataset_name     
        if dataset_name not in self.workspace.datasets:
            train_data_ds = train_data_ds.register(workspace=self.workspace,
                        name=dataset_name,
                        description=self.args.dataset_desc,
                        create_new_version=True)

        print('Train dataset:', train_data_ds)
        print('Train dataset tp path:', train_data_ds.to_path())
        print('Input dataset:', self.run.input_datasets)

        datastore = self.workspace.get_default_datastore()
        dataset = Dataset.File.from_files(datastore.path('beanleaf_dataset')).as_named_input('input')
        print('Dataset:', dataset)
        print('Path on compute:', dataset.path_on_compute)

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

        history = model.fit(train_ds, epochs = 1, validation_data = val_ds)
        plt.plot(history.history['accuracy'])
        plt.plot(history.history['val_accuracy'])
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train_acc', 'val_acc'], loc='best')
        self.run.log_image(name='acc_over_epochs.png', plot=plt)
        plt.show()

        # joblib.dump(model, self.args.model_path)
        model.save(self.args.model_path, save_format='tf')

        test_loss, test_acc = model.evaluate(test_ds)
        self.run.log(name='Test Accuracy', value=test_acc)
        self.run.log(name='Test Loss', value=test_loss)

        self.run.tag('BeanleafDiseaseClassifierFinalRun')

        match = re.search('([^\/]*)$', self.args.model_path)

        # Upload Model to Run artifacts
        self.run.upload_folder(name=self.args.artifact_loc,
                                path_or_stream=self.args.model_path)

        print('Run Files: ', self.run.get_file_names())
        self.run.complete()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='QA Code Indexing pipeline')
    parser.add_argument('--container_name', type=str, help='Path to default datastore container', default='beanleaf_dataset')
    parser.add_argument('--dataset_name', type=str, help='Dataset name to store in workspace', default='beanleaf')
    parser.add_argument('--dataset_desc', type=str, help='Dataset description', default='')
    parser.add_argument('--model_path', type=str, help='Path to store the model', default='./models/')
    parser.add_argument('--artifact_loc', type=str, 
                        help='DevOps artifact location to store the model', default='./outputs/models/')
    args = parser.parse_args()
    beanleaf_disease_classifier = BeanleafDiseaseClassifier(args)
    beanleaf_disease_classifier.create_pipeline()