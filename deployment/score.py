import os
import tensorflow as tf
import tensorflow_hub as hub

import numpy as np

import json
import traceback
import logging
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def init():
    global model
    global logger

    model_path = os.path.join(os.getenv('AZUREML_MODEL_DIR'), 'models')
    logger.info('Model Path:', model_path)
    model = tf.keras.models.load_model(model_path)
    logger.info('beanleaf_disease_classifier model loaded...')

def decode_img(image):
  img = tf.image.decode_jpeg(image, channels=3)  
  img = tf.image.resize(img,[224,224])
  return np.expand_dims(img, axis=0)

def create_response(predicted_lbl):
    classes=['angular_leaf_spot','bean_rust','healthy']
    resp_dict = {}
    logger.info('Predicted Class:', predicted_lbl[0])
    resp_dict['predicted_class'] = classes[predicted_lbl[0]]
    return json.loads(json.dumps({'output': resp_dict}))

def run(raw_data):
    try:
        logger.info('Request data:', raw_data)
        data = json.loads(raw_data)
        content = requests.get(data.path).content
        label =np.argmax(model.predict(decode_img(content)), axis=1)
        response = create_response(label)
        logger.info('Response:', response)
        return response

    except Exception as err:
        logger.error(err)
        traceback.print_exc()