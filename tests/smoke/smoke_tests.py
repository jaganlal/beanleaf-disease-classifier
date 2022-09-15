import requests
import json
import logging

req_sample = {'path': 'https://beanipm.pbgworks.org/sites/pbg-beanipm7/files/styles/picture_custom_user_wide_1x/public/AngularLeafSpotFig1a.jpg'}
classes = ['angular_leaf_spot','bean_rust','healthy']

def test_ml_service(scoreurl):
    assert scoreurl != None
    headers = {'Content-Type':'application/json'}
    resp = requests.post(scoreurl, data=json.loads(json.dumps(req_sample)), headers=headers)
    assert resp.status_code == requests.codes['ok']
    assert resp.text != None
    assert resp.headers.get('content-type') == 'application/json'
    assert int(resp.headers.get('Content-Length')) > 0

def test_prediction(scoreurl):
    assert scoreurl != None
    headers = {'Content-Type':'application/json'}
    resp = requests.post(scoreurl, data=json.loads(json.dumps(req_sample)), headers=headers)
    resp_json = json.loads(resp.text)
    assert resp_json['output']['predicted_class'] == 'angular_leaf_spot'
    logging.info(resp)