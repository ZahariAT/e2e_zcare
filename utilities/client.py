import logging

from typing import List
from requests import Session


class Client:
    def __init__(self, url: str, proxies: List[str] = None):
        self.session = Session()
        if proxies is not None:
            self.session.proxies.update(proxies)
        self.url = url

    def request(self, method,
                prefix: str = '',
                raw_response=False,
                json_response=False,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                json=None,
                ):

        logging.info(f'{method}: {self.url+prefix}')

        resp = self.session.request(method=method,
                                    url=self.url+prefix,
                                    params=params,
                                    data=data,
                                    headers=headers,
                                    cookies=cookies,
                                    files=files,
                                    auth=auth,
                                    timeout=timeout,
                                    allow_redirects=allow_redirects,
                                    proxies=proxies,
                                    hooks=hooks,
                                    stream=stream,
                                    verify=verify,
                                    cert=cert,
                                    json=json)
        logging.info(f'Response status: {resp.status_code}')
        logging.debug(f'Response body: {resp.content}')

        resp.raise_for_status()

        if raw_response:
            return resp
        if json_response:
            return resp.json()
        return resp.content

    def get(self, prefix: str = '', **params):
        return self.request('GET', prefix=prefix, **params)

    def post(self, prefix: str = '', data=None, json=None,  **params):
        return self.request('POST', prefix=prefix, data=data, json=json, **params)

    def put(self, prefix: str = '', data=None, **params):
        return self.request('PUT', prefix=prefix, data=data, **params)

    def delete(self, prefix: str = '', **params):
        return self.request('DELETE', prefix=prefix, **params)

    @property
    def cookies(self):
        return self.session.cookies
