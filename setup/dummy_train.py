
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import sys
import os
from os.path import exists
import tensorflow as tf

print("*********************************************************")
print("Hello Azure ML!")

mounted_input_path = sys.argv[1]
# mounted_output_path = sys.argv[2]

print("Argument 1: %s" % mounted_input_path)

path_to_file = os.path.join(mounted_input_path, '/beanleaf_dataset/train/healthy/healthy_train.0.jpg')
print("Path to file:", path_to_file)
file_exists = exists(path_to_file)
print("File healthy_train.0.jpg - ", file_exists)

path_to_file1 = os.path.join(mounted_input_path, 'beanleaf_dataset/train/healthy/healthy_train.0.jpg')
print("Path to file1:", path_to_file1)
file_exists1 = exists(path_to_file1)
print("File healthy_train.0.jpg 1 - ", file_exists1)

path_to_file2 = os.path.join(mounted_input_path, 'train/healthy/healthy_train.0.jpg')
print("Path to file2:", path_to_file2)
file_exists2 = exists(path_to_file2)
print("File healthy_train.0.jpg 2 - ", file_exists2)

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

print('Training DS')
print(train_ds)

# with open(mounted_input_path, 'r') as f:
#     content = f.read()
#     with open(os.path.join(mounted_output_path, 'output.csv'), 'w') as fw:
#         fw.write(content)
