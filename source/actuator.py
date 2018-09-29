"""
  The Actuator receives an OpenC2 command, performs the requested operation, and returns a response
"""

from time import ctime


def msg_dump(m, label):
    print('-----', label, '-----')
    if m['msg_type'] == 'response':
        print('  status =', m['status'])
    for f in ('content_type', 'msg_type', 'request_id', 'to', 'from', 'created', 'content'):
        print('  ' + f + ' =', m[f] if f in m else None)


def process_command(cmd):       # Process the OpenC2-Command, return status code and OpenC2-Response
    stat = 200
    rsp = {}
    feat = {    # Actuator's answers to query-features command
        'versions': ['1.0'],
        'profiles': ['oasis-open.org/openc2/v1.0/hello-world'],
        'pairs': ['query', ['features']],
        'schema': {
            'meta': {'module': 'oasis-open.org/openc2/v1.0/hello-world'},
            'types': [
                ['OpenC2-Command', 'Record', [], '', [
                    [1, 'action', 'Action', [], ''],
                    [2, 'target', 'Target', [], '']
                ]],
                ['Action', 'Enumerated', [], '', [
                    [6, 'query', '']
                ]],
                ['Target', 'Choice', [], '', [
                    [1, 'features', 'Feature', ['[0', ']0'], '']
                ]],
                ['Feature', 'Enumerated', [], '', [
                    [1, 'versions', ''],
                    [2, 'profiles', ''],
                    [3, 'pairs', ''],
                    [4, 'schema', '']
                ]],
                ['OpenC2-Response', 'Record', [], '', [
                    [1, 'status', 'Integer', [], ''],
                    [2, 'results', 'Results', [], '']
                ]],
                ['Results', 'Map', [], '', [
                    [1, 'versions', 'String', ['[0', ']0'], ''],
                    [2, 'profiles', 'String', ['[0', ']0'], ''],
                    [3, 'pairs', 'Pair', ['[0', ']0'], ''],
                    [4, 'schema', 'jadn:Schema', [], '']
                ]],
                ['Pair', 'Array', [], '', [
                    [1, 'action', 'Enumerated', ['*Action'], ''],
                    [2, 'targets', 'Enumerated', ['*Target', [']0']], '']
                ]]
            ]
        }
    }
    try:
        result = {}
        assert cmd['action'] == 'query'
        for i in cmd['target']['features']:
            result.update({i: feat[i]})
        rsp = {'result': result}
    except (AssertionError, KeyError):
        stat = 501
    rsp.update({'status': stat})
    return stat, rsp


def actuator(cm):       # Process the message containing the command, return the result message
    msg_dump(cm, 'command')
    assert cm['content_type'] == 'openc2'
    assert cm['msg_type'] == 'request'

    stat, resp = process_command(cm['content'])

    rm = {'status': stat, 'content': resp, 'content_type': cm['content_type'], 'msg_type': 'response'}
    rm.update({'request_id': cm['request_id']})
    rm.update({'created': cm['created'] + 2000 if cm['created'] else None})
    rm.update({'from': 'Ham_95', 'to': cm['from']})
    msg_dump(rm, 'response')
    return rm