import json
import requests
from time import time, ctime
from urllib.parse import urlparse
from ham_server_http import ms_to_date

http_hdr_map = {
    'request_id': 'X-Correlation-ID',
    'from': 'Authorization',
    'to': 'To'
}


def send_msg(dest, msg):
    m = {
        'content': None,
        'content_type': 'openc2',
        'msg_type': 'request',
        'request_id': None,
        'created': int(1000*time()),
        'from': None,
        'to': None
    }
    m.update(msg)
    assert m['msg_type'] in ['request', 'response', 'notification']
    assert m['content']
    u = urlparse(dest)
    transfer[u.scheme](dest, m)


def send_https(dest, msg):
    mt = {'request': '-cmd', 'response': '-rsp', 'notification': '-not'}[msg['msg_type']]
    hdr = {http_hdr_map[h]: str(msg[h]) for h in ['request_id', 'to', 'from'] if msg[h]}
    hdr.update({'Date': ms_to_date(msg['created'])})
    hdr.update({'Content-Type': 'application/' + msg['content_type'] + mt + '+json'})
    d = json.dumps(msg['content'])
    hdr.update({'Content-Length': str(len(d))})
    print('Request Headers =', hdr)
    print('Request =', d)

    r = requests.get(dest, headers=hdr, data=d)

    print('Status =', r.status_code)
    print('Response Headers =', r.headers)
    print('Response =', r.text)


def send_coap(dest, msg):
    print('CoAP Transfer Spec not implemented')


def send_mqtt(dest, msg):
    print('MQTT Transfer Spec not implemented')


def send_file(dest, msg):
    print('File Transfer Spec not implemented')


transfer = {
    'http': send_https,
    'coap': send_coap,
    'mqtt': send_mqtt,
    'file': send_file,
}


if __name__ == '__main__':
    destination = 'http://localhost:8000/api'
    content = {'action': 'query', 'target': {'features': ['profiles']}}
    message = {
        'content': content,
        'request_id': '25348',
        'from': 'MyOrchestrator_342'
    }
    send_msg(destination, message)
