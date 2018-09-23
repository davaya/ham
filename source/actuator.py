"""
  The Actuator receives an OpenC2 command, performs the requested operation, and returns a response
"""

from time import ctime


def msg_dump(m, label):
    print('-----', label, '-----')
    if m['msg_type'] == 'response':
        print('  status =', m['status'])
    for f in ('content_type', 'msg_type', 'correlation_id', 'to', 'from', 'created', 'content'):
        print('  ' + f + ' =', m[f])
    print('--------------------')


def process_command(cmd):
    stat = 200
    resp = {'status': stat, 'result': 'stuff'}
    return stat, resp


def actuator(cm):
    msg_dump(cm, "command")
    assert cm['content_type'] == 'openc2'
    assert cm['msg_type'] == 'request'
    assert cm['correlation_id']

    stat, resp = process_command(cm['content'])

    rm = {'status': stat, 'content': resp}
    rm.update({'content_type': cm['content_type'], 'msg_type': 'response', 'correlation_id': cm['correlation_id']})
    rm.update({'from': None, "to": None, "created": None})
    msg_dump(rm, "response")
    return rm