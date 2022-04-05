from mindsync.api import Api, RENT_FIXED, RENT_DYNAMIC
from envs import API_KEY, BASE_URL
import re, time, os, sys


CODE = b'''
#!/usr/bin/env python

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

    print(f'\033[34m> Stopping rent\033[0m')
    rv = api.stop_rent(rent_id=rent_id, meta=True)
    print(rv)


if __name__ == '__main__':
    main()
