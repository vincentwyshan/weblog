# coding=utf8

import os
import hashlib
import cPickle
import time


_ROOTDIR = "/tmp/weblog"
if not os.path.exists(_ROOTDIR):
    os.makedirs(_ROOTDIR)


def cache_view(timeout):
    def call(func):
        def wraper(*karg, **kwargs):
            request = karg[1]
            path = request.path
            key = hashlib.md5(path).hexdigest()
            path = os.path.join(_ROOTDIR, key)
            if os.path.exists(path) and check_mtime(path, timeout):
                return cPickle.load(open(path, 'rb'))
            else:
                result = func(request)
                cPickle.dump(result, open(path, 'wb'))
                return result
        return wraper
    return call


def check_mtime(path, timeout):
    st_time = os.stat(path).st_mtime
    if (st_time + timeout) < time.time():
        return False
    return True