import os
from azureml.core import Datastore, Dataset
from azureml.core.run import Run
import argparse
import logging

import tensorflow as tf
import matplotlib.pyplot as plt
import tensorflow_hub as hub

import warnings
warnings.filterwarnings('ignore')

class BeanleafDiseaseClassifier():
    def __init__(self, args):
        self.args = args
        self.run = Run.get_context()
        self.workspace = self.run.experiment.workspace

    def create_pipeline(self):
        batch_size = 128
        img_height = 224
        img_width = 224

        self.datastore = Datastore.get(self.workspace, self.workspace.get_default_datastore().name)
        datastore_paths = [(self.datastore, self.args.container_name)]
        beanleaf_ds = Dataset.File.from_files(path=datastore_paths)

        mount_point = None

        with beanleaf_ds.mount() as mount_context:
            mount_point = mount_context.mount_point

            if mount_point is None:
                print('Mount failed...')
                return

            beanleaf_dataset_train_path = os.path.join(mount_point, 'train')
            beanleaf_dataset_test_path = os.path.join(mount_point, 'test')
            beanleaf_dataset_validation_path = os.path.join(mount_point, 'validation')

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

            history = model.fit(train_ds, epochs = 16, validation_data = val_ds)
            plt.plot(history.history['accuracy'])
            plt.plot(history.history['val_accuracy'])
            plt.ylabel('accuracy')
            plt.xlabel('epoch')
            plt.legend(['train_acc', 'val_acc'], loc='best')
            plt.savefig('./outputs/acc_over_epochs.png')
            self.run.log_image(name='acc_over_epochs.png', plot=plt)

            model.save(self.args.model_path, save_format='tf')

            test_loss, test_acc = model.evaluate(test_ds)
            self.run.log(name='Test Accuracy', value=test_acc)
            self.run.log(name='Test Loss', value=test_loss)

            self.run.tag('BeanleafDiseaseClassifierFinalRun')

            # Upload Model to Run artifacts
            self.run.upload_folder(name=self.args.artifact_loc,
                                    path=self.args.model_path)

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