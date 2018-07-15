from email.mime.image import MIMEImage
from urllib.parse import quote
from uuid import uuid4

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def cid_static(context, path):
    '''
    Embed a file from static files.
    '''
    fin = staticfiles_storage.open(path)
    return _embed_cid(context, fin)


@register.simple_tag(takes_context=True)
def cid_media(context, field):
    '''
    Embed a file from a FileField / ImageField
    '''
    fin = field.open()
    return _embed_cid(context, fin)


def _embed_cid(context, fobj):
    '''
    Generates a CID URI, and stores the MIME attachment in the context.request_context
    '''
    cid = uuid4()

    if 'cid' not in context.render_context:
        context.render_context['cid'] = []

    mime = MIMEImage(fobj.read())
    mime['Content-ID'] = '<{}>'.format(quote(str(cid)))

    context.render_context['cid'].append(mime)

    return 'cid:{}'.format(cid)