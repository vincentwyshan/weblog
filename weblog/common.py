# coding=utf8

from pyramid.i18n import TranslationStringFactory


_ = TranslationStringFactory('weblog')


def _t(request, trans):
    return request.localizer.translate(_(trans))


