import os
from io import BytesIO
from collections import namedtuple

from PIL import Image
from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory("weblog")

img_static = namedtuple(
    "img_static",
    ["raw", "desktop_dir", "desktop_width", "mobile_dir", "mobile_width"],
)
img_static = img_static(
    raw="static",
    desktop_dir="static-desktop",
    desktop_width=1280,
    mobile_dir="static-mobile",
    mobile_width=500,
)


def _t(request, trans):
    return request.localizer.translate(_(trans))


def thumbnail(raw, max_size=800):
    """

    :param raw: Readable image IO(for example: StringIO)
    :param max_size: Max size for thumbnail
    :return:
    """
    size = (max_size, max_size)
    raw = BytesIO(raw)
    im = Image.open(raw)
    im.thumbnail(size, Image.ANTIALIAS)
    out = BytesIO()

    if im.mode in ('RGBA', 'LA'):
        im = im.convert('RGB')

    im.save(out, "JPEG")
    return out.getvalue()


def test(path):
    raw = open(path, "rb").read()
    path, ext = os.path.splitext(path)
    open(path + ".thumbnail" + ext, "wb").write(thumbnail(raw))
