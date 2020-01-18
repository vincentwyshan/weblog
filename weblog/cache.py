# coding=utf8

import os
import hashlib
import pickle
import time


_ROOTDIR = os.environ.get("WEBLOG_CACHE_DIR", "/tmp/weblogcache")
if not os.path.exists(_ROOTDIR):
    os.makedirs(_ROOTDIR)
_IMAGE_DIR = os.path.join(_ROOTDIR, "images")
if not os.path.exists(_IMAGE_DIR):
    os.makedirs(_IMAGE_DIR)


def cache_view(timeout):
    def call(func):
        def wraper(*karg, **kwargs):
            request = karg[1]
            if request.registry.settings["USER_NAME"] == "test":
                return func(request)
            path = request.path
            locale_name = request.localizer.locale_name or ""
            key = hashlib.md5(path + locale_name).hexdigest()
            path = os.path.join(_ROOTDIR, key)
            if os.path.exists(path) and check_mtime(path, timeout):
                return pickle.load(open(path, "rb"))
            else:
                result = func(request)
                pickle.dump(result, open(path, "wb"))
                return result

        return wraper

    return call


def check_mtime(path, timeout):
    st_time = os.stat(path).st_mtime
    if (st_time + timeout) < time.time():
        return False
    return True
