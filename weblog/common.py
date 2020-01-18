# coding=utf8

import os
from io import StringIO

from PIL import Image
from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory("weblog")


def _t(request, trans):
    return request.localizer.translate(_(trans))


def thumbnail(raw, max_size=800):
    """

    :param raw: Readable image IO(for example: StringIO)
    :param max_size: Max size for thumbnail
    :return:
    """
    size = (max_size, max_size)
    raw = StringIO(raw)
    im = Image.open(raw)
    im.thumbnail(size, Image.ANTIALIAS)
    out = StringIO()
    im.save(out, "JPEG")
    return out.getvalue()


def test(path):
    raw = open(path, "rb").read()
    path, ext = os.path.splitext(path)
    open(path + ".thumbnail" + ext, "wb").write(thumbnail(raw))
