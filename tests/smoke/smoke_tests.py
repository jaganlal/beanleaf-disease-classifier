import requests
import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

req_sample = {'path': 'https://beanipm.pbgworks.org/sites/pbg-beanipm7/files/styles/picture_custom_user_wide_1x/public/AngularLeafSpotFig1a.jpg'}
classes = ['angular_leaf_spot','bean_rust','healthy']

def test_ml_service(scoreurl):
    assert scoreurl != None
    headers = {'Content-Type':'application/json'}
    prediction_request = json.loads(json.dumps(req_sample))
    logger.info('Test ml service request:', json.dumps(req_sample))
    resp = requests.post(scoreurl, json=prediction_request, headers=headers)
    logger.info('ML service response:', resp.status_code)
    logger.debug('ML service response - DEBUG:', resp.status_code)
    assert resp.status_code == requests.codes['ok']
    assert resp.text != None
    assert resp.headers.get('content-type') == 'application/json'
    assert int(resp.headers.get('Content-Length')) > 0

def test_prediction(scoreurl):
    assert scoreurl != None
    headers = {'Content-Type':'application/json'}
    prediction_request = json.loads(json.dumps(req_sample))
    logger.info('Test prediction request:', json.dumps(req_sample))
    resp = requests.post(scoreurl, json=prediction_request, headers=headers)
    logger.info('Test prediction response:', resp.text)
    resp_json = json.loads(resp.text)
    assert resp_json['output']['predicted_class'] == 'angular_leaf_spot'