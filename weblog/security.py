import re
from hashlib import md5

from pyramid.response import Response


def auth(func):
    def _warper(*kargs, **kwarg):
        request = kargs[1]
        user_name = request.registry.settings["USER_NAME"]
        password = request.registry.settings["USER_PWD"]
        auth_str = request.headers.get("Authorization")
        if (
            "Authorization" not in request.headers
            or not digest_http_auth_valid(
                auth_str, request.method, user_name, password
            )
        ):
            html = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
            "http://www.w3.org/TR/1999/REC-html401-19991224/loose.dtd">
        <HTML>
            <HEAD>
            <TITLE>Error</TITLE>
            <META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=utf-8">
            </HEAD>
            <BODY><H1>401 Unauthorized.</H1></BODY>
        </HTML>"""
            response = Response(html)
            response.status_int = 401
            # response.headerlist.append(('WWW-Authenticate',
            # 'Basic realm="Secure Area"'))
            tokens = digest_http_auth_tokens()
            remote_addr = request.remote_addr.encode("utf-8")
            tokens["nonce"] = md5(remote_addr).hexdigest()
            auth_str = "Digest " + ",".join(
                ['%s="%s"' % (k, v) for k, v in tokens.items()]
            )
            response.headerlist.append(("WWW-Authenticate", auth_str))
        else:
            response = func(request)
        return response

    return _warper


def digest_http_auth_valid(auth_str, method, user_name, user_pwd):
    """response=MD5(HA1:nonce:nonceCount:clientNonce:qop:HA2)
    HA1=MD5(username:realm:password)
    HA2=MD5(method:digestURI)
    refreence: http://en.wikipedia.org/wiki/Digest_access_authentication
    """
    data = digest_http_auth_parse(auth_str)
    data.update({"password": user_pwd})

    if data["username"] != user_name:
        return False

    ha1_data = "%(username)s:%(realm)s:%(password)s" % data
    HA1 = md5(ha1_data.encode("utf-8"))
    ha2_data = "%s:%s" % (method, data["uri"])
    HA2 = md5(ha2_data.encode("utf-8"))

    data.update(dict(HA1=HA1.hexdigest(), HA2=HA2.hexdigest()))
    combine = "%(HA1)s:%(nonce)s:%(nc)s:%(cnonce)s:%(qop)s:%(HA2)s" % data

    response = md5(combine.encode("utf-8")).hexdigest()
    return response == data["response"]


def digest_http_auth_parse(auth_str):
    auth_str = auth_str.replace("Digest", "")
    token_list = auth_str.split(",")
    result = {}
    for t in token_list:
        m = re.search("\s*(?P<name>[^=]+)=(?P<val>.+)", t)
        val = m.group("val").strip()
        if val[0] == val[-1] and val[0] in ('"', "'"):
            val = val[1:-1]
        result[m.group("name")] = val
    return result


def digest_http_auth_tokens():
    realm = "Blog Auth"
    qop = "auth"
    nonce = None
    opaque = "1053267b-17a6-414e-9a75-c61b66f445bb"
    return locals()

