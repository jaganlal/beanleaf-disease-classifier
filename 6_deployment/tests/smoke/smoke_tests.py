import requests
import json

req_sample = {'path': 'https://extension.umn.edu/sites/extension.umn.edu/files/bacterial-brown-spot-bean.jpg'}
classes = ['angular_leaf_spot','bean_rust','healthy']

def test_ml_service(scoreurl):
    assert scoreurl != None
    headers = {'Content-Type':'application/json'}
    resp = requests.post(scoreurl, json=req_sample, headers=headers)
    assert resp.status_code == requests.codes['ok']
    assert resp.text != None
    assert resp.headers.get('content-type') == 'application/json'
    assert int(resp.headers.get('Content-Length')) > 0

def test_prediction(scoreurl):
    assert scoreurl != None
    headers = {'Content-Type':'application/json'}
    resp = requests.post(scoreurl, json=req_sample, headers=headers)
    resp_json = json.loads(resp.text)
    assert resp_json['output']['predicted_class'] == 'bean_rust'