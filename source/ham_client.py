import json
import requests
from time import time, ctime
from urllib.parse import urlparse


def send_msg(dest, msg):
    m = {
        'content': None,
        'content_type': 'openc2',
        'correlation_id': None,
        'created': int(1000*time()),
        'from': None,
        'msg_type': 'request',
        'to': None
    }
    m.update(msg)
    msg_dump(m)
    assert m['msg_type'] in ['request', 'response', 'notification']
    assert m['content']
    u = urlparse(dest)
    transfer[u.scheme](dest, m)


def send_https(dest, msg):
    ct = {'request': '-cmd', 'response': '-rsp', 'notification': '-not'}[msg['msg_type']]
    hdr = {h: str(msg[h]) for h in ['correlation_id', 'created', 'to', 'from'] if msg[h]}
    hdr.update({'content-type': msg['content_type'] + ct + '+json'})
    d = json.dumps(msg['content'])
    hdr.update({'content-length': str(len(d))})
    r = requests.get(dest, headers=hdr, data=d)
    print('Status =', r.status_code)
    print('Headers =', r.headers)
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


def msg_dump(m):
    print('----------')
    print('  Content =', m['content'])
    print('  Content Type =', m['content_type'])
    print('  Message Type =', m['msg_type'])
    print('  Correlation ID =', m['correlation_id'])
    print('  To =', m['to'])
    print('  From =', m['from'])
    print('  Created =', ctime(m['created']/1000))
    print('----------')


if __name__ == '__main__':
    destination = 'http://localhost:8000/api'
    content = {'action': 'query', 'target': {'openc2': ['profiles']}}
    message = {
        'content': content,
        'correlation_id': '25348',
        'from': 'MyOrchestrator_342'
    }
    send_msg(destination, message)
