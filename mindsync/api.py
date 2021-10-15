from __future__ import absolute_import

import aiohttp
import logging
import asyncio
from urllib.parse import urljoin


class MindsyncApiError(RuntimeError):
    pass


def _purge(obj):
    if isinstance(obj, dict):
        return dict((k, _purge(v)) for k, v in obj.items() 
                    if (not isinstance(v, dict) and v is not None) or (isinstance(v, dict) and v))
    else:
        return obj


DEFAULT_BASE_URL = 'https://api.mindsync.ai'


class AsyncApi:
    def __init__(self, key, base_url=DEFAULT_BASE_URL):
        self.__logger = logging.getLogger(__name__)
        self.__key = key
        self.__base_url = base_url

    
    async def profile(self, user_id=None):
        '''Gets profile.

        @param user_id User identifier to get profile for.
        @return Returns profile specified by user_id or own profile if user_id is None by default.
        '''

        url = urljoin(self.__base_url, '/api/1.0/users/client/profile' 
                      if user_id is None else f'/api/1.0/users/client/profile/{user_id}')
        try:
            async with aiohttp.request(method='GET', url=url, 
                                       headers={'api-key': self.__key}, 
                                       raise_for_status=True) as resp:
                    result = await resp.json()
                    return result['result']
        except Exception as e:
            self.__logger.debug(f'Unable to get profile [{repr(e)}]')
            raise MindsyncApiError('Unable to get profile') from e


    async def set_profile(self, *, first_name=None, last_name=None, phone=None, gravatar=None, 
                          nickname=None, wallet_symbol=None, wallet_address=None, country=None, city=None):
        '''Sets profile info.'''

        args = dict(lastName=last_name, 
                    firstName=first_name, 
                    phone=phone, 
                    gravatar=gravatar, 
                    nickname=nickname, 
                    wallet=dict(symbol=wallet_symbol, address=wallet_address), 
                    country=country,
                    city=city)

        args = _purge(_purge(args))
        if not args:
            raise MindsyncApiError('Invalid arguments, nothing to set')

        try:
            async with aiohttp.request(method='PUT', 
                                       url=urljoin(self.__base_url, '/api/1.0/users/client/profile'),
                                       json=args, 
                                       headers={'api-key': self.__key}, 
                                       raise_for_status=True) as resp:
                    result = await resp.json()
                    return result['result']
        except Exception as e:
            self.__logger.debug(f'Unable to set profile [{repr(e)}]')
            raise MindsyncApiError('Unable to set profile') from e


class Api:
    def __init__(self, key, base_url=DEFAULT_BASE_URL):
        self.__async_api = AsyncApi(key, base_url)

    def profile(self):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self.__async_api.profile())
