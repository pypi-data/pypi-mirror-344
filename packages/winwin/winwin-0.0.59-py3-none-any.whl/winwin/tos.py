import warnings
from typing import Optional, Union
from urllib.parse import urlparse

import importlib

tos = importlib.import_module("tos")
import tosfs


class TosUri:
    def __init__(self, bucket: str, path: str):
        self.bucket = bucket
        self.path = path.lstrip("/")

    def __str__(self):
        return f"tos://{self.bucket}/{self.path}"

    @classmethod
    def from_path(cls, path: str, bucket: Optional[str] = None):
        if path.startswith("tos://"):
            result = urlparse(path)
            return cls(result.netloc, result.path)
        return cls(bucket, path)

    @property
    def full_path(self):
        return f"/{self.bucket}/{self.path}"


class TosFs:
    def __init__(self, access_key: str, secret_key: str, endpoint: str, region: str, bucket: str = 'winwin-algo'):
        self._access_key = access_key
        self._secret_key = secret_key
        self._endpoint = endpoint
        self._region = region
        self._bucket_name = bucket
        self._client = None
        self.fs = tosfs.TosFileSystem(
            endpoint=self._endpoint,
            key=self._access_key,
            secret=self._secret_key,
            region=self._region,
        )

    @property
    def endpoint(self) -> str:
        return self._endpoint

    @property
    def external_endpoint(self) -> str:
        # TOS endpoints typically don't have internal/external distinction like OSS
        # Return the same endpoint unless specific external endpoint is needed
        return self._endpoint

    @property
    def client(self) -> tos.TosClientV2:
        if not self._client:
            self._client = self.client_for(self._bucket_name)
        return self._client

    def client_for(self, bucket_name: str, external: bool = False) -> tos.TosClientV2:
        return tos.TosClientV2(
            ak=self._access_key,
            sk=self._secret_key,
            endpoint=self.external_endpoint if external else self.endpoint,
            region=self._region,
        )

    def _build_uri(self, path) -> TosUri:
        return TosUri.from_path(path, self._bucket_name)

    def _full_path(self, path) -> str:
        return self._build_uri(path).full_path

    def _replace_path(self, p):
        p["Key"] = p["name"] = "tos:/" + p["name"]
        return p

    def write(self, path, data):
        uri = self._build_uri(path)
        if uri.bucket == self._bucket_name:
            resp = self.client.put_object(uri.bucket, uri.path, content=data)
            assert resp.status_code == 200, f"Failed to write to {path}: {resp.status_code}"
        else:
            client = self.client_for(uri.bucket)
            resp = client.put_object(uri.bucket, uri.path, content=data)
            assert resp.status_code == 200, f"Failed to write to {path}: {resp.status_code}"

    def open(self, path, mode=None):
        if mode is None or mode == "rb":
            uri = self._build_uri(path)
            if uri.bucket == self._bucket_name:
                return self.client.get_object(uri.bucket, uri.path)
            return self.client_for(uri.bucket).get_object(uri.bucket, uri.path)
        warnings.warn(
            f"TosFs.open({path}, {mode}) is deprecated, use write or read instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.fs.open(self._full_path(path), mode)

    def exists(self, path):
        return self.fs.exists(self._full_path(path))

    def isdir(self, path):
        return self.fs.isdir(self._full_path(path))

    def isfile(self, path):
        return self.fs.isfile(self._full_path(path))

    def copy(self, src, dst, recursive=False):
        self.fs.copy(self._full_path(src), self._full_path(dst), recursive)

    def listdir(self, path):
        return [self._replace_path(p) for p in self.fs.listdir(self._full_path(path))]

    def stat(self, path):
        """
        stat returns:
        {
            "name": "tos://bucket/test/test.txt",
            "type": "file",
            "size": 11,
            "LastModified": 1740624773,
            "Size": 11,
            "Key": "tos://bucket/test/test.txt"
        }
        """
        uri = self._build_uri(path)
        if uri.bucket != self._bucket_name:
            client = self.client_for(uri.bucket)
        else:
            client = self.client
        try:
            meta = client.head_object(uri.bucket, uri.path)
            return {
                "name": str(uri),
                "type": "file",
                "size": meta.content_length,
                "LastModified": meta.last_modified,
                "Size": meta.content_length,
                "Key": str(uri),
            }
        except tos.exceptions.TosServerError as e:
            if e.status_code == 404:
                return self._replace_path(self.fs.stat(self._full_path(path)))
            raise

    def rm(self, path: Union[str, list[str]], recursive=False, maxdepth=None):
        if isinstance(path, str):
            self.fs.rm(self._full_path(path), recursive, maxdepth)
        else:
            self.fs.rm([self._full_path(p) for p in path], recursive, maxdepth)

    def absolute_path(self, path) -> str:
        return str(self._build_uri(path))

    def sign_url(self, path, expires=864000):
        uri = self._build_uri(path)
        client = self.client_for(uri.bucket, True)
        return client.pre_signed_url("GET", uri.bucket, uri.path, expires)
