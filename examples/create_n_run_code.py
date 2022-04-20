#!/usr/bin/env python3

'''The example shows how to create a custom python code, 
start rent and execute the code by using Mindsync API.
'''


from mindsync.api import Api, RENT_FIXED, RENT_DYNAMIC
from envs import API_KEY, BASE_URL
import re, time, os, sys
import requests


CODE = b'''

print('Hi there!')

'''


RIG_ID = 'vd2zRBZrJE1'
APP_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


def main():
    api = Api(key=API_KEY, base_url=BASE_URL, raise_for_error=True)

    # result = api.create_code(file=CODE, meta=True)
    print('\033[34m> Creating code\033[0m')
    rv = api.create_code(file=os.path.join(APP_DIR, 'script.py'), meta=True)
    print(rv)

    assert 'result' in rv, 'No result key'
    assert 'hash' in rv['result'], 'No hash key in result'
    code_id = rv['result']['hash']

    print('\033[34m> Getting rig price\033[0m')
    rv = api.rig_price(rig_id=RIG_ID, meta=True)
    print(rv)

    print('\033[34m> Starting rent\033[0m')
    rv = api.start_rent(rig_id=RIG_ID, tariff_name=RENT_DYNAMIC, meta=True)
    print(rv)

    assert 'result' in rv, 'No result key'
    assert 'hash' in rv['result'], 'No hash key in result'
    assert 'proxyUrl' in rv['result'], 'No proxy url key in result'
    rent_id = rv['result']['hash']
    proxy_url = rv['result']['proxyUrl']
    m = re.search('([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', proxy_url)
    rent_uuid = m[0]

    wait = True
    while wait:
        print(f'\033[34m> Getting rent state {rent_uuid}\033[0m')
        rv = api.rent_state(uuid=rent_uuid, meta=True)
        print(rv)
        assert 'result' in rv, 'No result key'
        assert 'name' in rv['result']
        if rv['result']['name'] == 'started':
            break

        time.sleep(1)

    print(f'\033[34m> Running code\033[0m')
    rv = api.run_code(code_id=code_id, rent_id=rent_id, meta=True)
    print(rv)

    wait = True
    while wait:
        print(f'\033[34m> Getting rent states {rent_uuid}\033[0m')
        rv = api.rent_states(uuid=rent_uuid, meta=True)
        print(rv)
        assert 'result' in rv, 'No result key'
        assert 'stateList' in rv['result']
        print(rv['result']['stateList'][-1]['name'])
        if rv['result']['stateList'][-1]['name'] == 'code_execute_finished' or rv['result']['stateList'][-1]['name'] == 'code_execute_failed':
            break

        time.sleep(1)

    print(f'\033[34m> Stopping rent\033[0m')
    rv = api.stop_rent(rent_id=rent_id, meta=True)
    print(rv)

    print(f'\033[34m> Getting code info\033[0m')
    rv = api.code_info(code_id=code_id, meta=True)
    print(rv)

    print(f'\033[34m> Log\033[0m')
    log_link = rv['result']['executionLogList'][-1]['link']
    print(log_link)
    r = requests.get(log_link)
    print(str(r.content, 'utf-8'))
    assert str(r.content, 'utf-8') == 'Hi there 12345!'


if __name__ == '__main__':
    main()
