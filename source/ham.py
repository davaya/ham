import requests
from time import time, ctime


def send_params(host='http://localhost/oc2',
                content=None,
                content_type='openc2',
                correlation_id=None,
                created=int(1000*time()),
                sent_from='orc1',
                msg_type='request',
                sent_to=None):
    print('Content =', content)
    print('Content Type =', content_type)
    print('Message Type =', msg_type)
    print('Correlation ID =', correlation_id)
    print('To =', sent_to)
    print('From =', sent_from)
    print('Created =', ctime(created/1000))

    assert msg_type in ['request', 'response', 'notification']
    r = requests.get(host)


def send_dict(host='http://localhost/oc2', params={}):
    msg = {
        'content': None,
        'content_type': 'openc2',
        'correlation_id': None,
        'created': int(1000*time()),
        'from': 'orc1',
        'msg_type': 'request',
        'to': None
    }
    msg.update(params)

    rsp = ''
    return rsp


if __name__ == '__main__':
    send_params(content={'action': 'deny'}, correlation_id='25348', sent_from='MyOrchestrator_342')
