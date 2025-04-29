import functools
import time
import requests
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Dict

from kumori.qcloud import sig_v1, errors


class Console:
    enabled_errors = True

    def __init__(self, domain="tencentcloudapi.com"):
        self.domain = domain
        self.services = {}

    def add_service(self, name, version):
        s = self.services[name] = Service(name, version, name + "." + self.domain)
        return s

    def get_service(self, name):
        return self.services[name]

    @contextmanager
    def suppress_errors(self):
        self.enabled_errors = False
        try:
            yield
        finally:
            self.enabled_errors = True


class Api:
    def __init__(self, name: str, version: str, method="POST"):
        self.name = name
        self.version = version
        self.method = method


class Service:
    def __init__(self, name: str, version: str, domain: str, scheme="https", port=None):
        self.name = name
        self.version = version
        self.domain = domain
        self.scheme = scheme
        self.port = port
        self.actions = {}

    @property
    def url(self):
        if self.port:
            return f"{self.scheme}://{self.domain}:{self.port}/"
        else:
            return f"{self.scheme}://{self.domain}/"

    def add_api(self, name, version=None, method="POST"):
        api = self.actions[name] = Api(name, version or self.version, method.upper())
        return api

    def get_api(self, name):
        api = self.actions.get(name, None)
        if not api:
            api = self.add_api(name)
        return api


console = Console()
console.add_service("cvm", "2017-03-12")


class User:
    def __init__(self, sid: str, skey: str, region: str, console=console, uin=None):
        if not sid or not skey:
            raise ValueError("missing sid or skey")
        self.console = console
        self.sid = sid
        self.skey = skey.encode("utf-8")
        self.region = region
        self.uin = uin

    def __getattr__(self, name):
        return UserContext(self, self.console.get_service(name))


class UserContext:
    verify_ssl = True

    def __init__(self, user: User, service: Service):
        self.user = user
        self.service = service
        self.headers = {}

    def prepare_params(self, api: Api, timestamp, nonce, kwargs):
        params = sig_v1.compose(
            kwargs,
            api.name,
            timestamp,
            nonce,
            self.user.region,
            api.version,
            self.user.sid,
        )
        signature = sig_v1.sign(
            self.user.skey, api.method, self.service.domain, "/", params
        )
        params["Signature"] = signature.decode()
        return params

    def get_action(self, name):
        api = self.service.get_api(name)
        url = self.service.url

        def func(**kwargs):
            params = self.prepare_params(api, int(time.time()), 114514, kwargs)
            if api.method == "GET":
                resp = requests.get(
                    url, params=params, headers=self.headers, verify=self.verify_ssl
                )
            elif api.method == "POST":
                resp = requests.post(
                    url, data=params, headers=self.headers, verify=self.verify_ssl
                )
            else:
                raise NotImplementedError

            if resp.status_code != 200:
                raise errors.ApiError("http status error")

            data = resp.json()["Response"]
            error = data.get("Error", None)
            if error and self.user.console.enabled_errors:
                msg = error["Message"]
                raise errors.ApiError(msg, error)
            return data

        return func

    def __getattr__(self, name):
        return self.get_action(name)
