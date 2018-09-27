"""
  The Actuator receives an OpenC2 command, performs the requested operation, and returns a response
"""

from time import ctime


def msg_dump(m, label):
    print('-----', label, '-----')
    if m['msg_type'] == 'response':
        print('  status =', m['status'])
    for f in ('content_type', 'msg_type', 'correlation_id', 'to', 'from', 'created', 'content'):
        print('  ' + f + ' =', m[f] if f in m else None)
    print('--------------------')


def process_command(cmd):
    target = next(iter(cmd['target']))
    if cmd['action'] == 'query' and target == 'features':
        stat = 200
        res = {}
        for i in cmd['target']['features']:
            res.update({i: 'foo'})
        resp = {'result': res}
    else:
        stat = 500
        resp = {'status_txt': '"' + cmd['action'] + ' ' + target + '" Not Supported'}
    resp.update({'status': stat})
    return stat, resp


def actuator(cm):
    msg_dump(cm, 'command')
    assert cm['content_type'] == 'openc2'
    assert cm['msg_type'] == 'request'

    stat, resp = process_command(cm['content'])

    rm = {'status': stat, 'content': resp, 'content_type': cm['content_type'], 'msg_type': 'response'}
    rm.update({'correlation_id': cm['correlation_id'] if 'correlation_id' in cm else None})
    rm.update({'from': 'Ham_95', 'to': cm['from'], 'created': None})
    msg_dump(rm, 'response')
    return rm