
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import sys
import os
from os.path import exists
import tensorflow as tf

print("*********************************************************")
print("Hello Azure ML!")

mounted_input_path = sys.argv[1]

print("Argument 1: %s" % mounted_input_path)

path_to_file = os.path.join(mounted_input_path, 'train/healthy/healthy_train.0.jpg')
print("Path to file2:", path_to_file)
file_exists = exists(path_to_file)
print("File healthy_train.0.jpg - ", file_exists)

batch_size = 128
img_height = 224
img_width = 224

training_path = os.path.join(mounted_input_path, 'train')
training_path_exists = exists(training_path)
print("training_path_exists - ", training_path_exists)

train_ds = tf.keras.preprocessing.image_dataset_from_directory(training_path,
                                                        seed=111,
                                                        image_size=(img_height, img_width),
                                                        batch_size=batch_size)