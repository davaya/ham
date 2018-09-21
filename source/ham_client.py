import requests
from time import time, ctime
from urllib.parse import urlparse


def send_msg(destination, message):
    m = {
        'content': None,
        'content_type': 'openc2',
        'correlation_id': None,
        'created': int(1000*time()),
        'from': None,
        'msg_type': 'request',
        'to': None
    }
    m.update(message)
    msg_dump(m)
    assert m['msg_type'] in ['request', 'response', 'notification']
    assert m['correlation_id'] != None
    u = urlparse(destination)
    transfer[u.scheme](destination, m)


def send_https(destination, message):
    r = requests.get(destination)
    print('Status =', r.status_code)
    print('Headers =', r.headers)
    print('Response =', r.text)


def send_coap(destination, message):
    print('CoAP Transfer Spec not implemented')


def send_mqtt(destination, message):
    print('MQTT Transfer Spec not implemented')


def send_file(destination, message):
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
    content = {'action': 'deny'}
    message = {
        'content': content,
        'correlation_id': '25348',
        'from': 'MyOrchestrator_342'
    }
    send_msg(destination, message)
