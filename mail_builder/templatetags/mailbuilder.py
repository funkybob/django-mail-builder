from email.mime.image import MIMEImage
from mimetypes import guess_type
from urllib.parse import quote
from uuid import uuid4

from django.contrib.staticfiles.storage import staticfiles_storage
from django.template import Library

register = Library()


@register.simple_tag(takes_context=True)
def cid_static(context, path, mimetype=None):
    '''
    Embed a file from static files.
    '''
    fin = staticfiles_storage.open(path)
    if mimetype is None:
        mimetype, _ = guess_type(path)
    return _embed_cid(context, fin, mimetype)


@register.simple_tag(takes_context=True)
def cid_media(context, field, mimetype=None):
    '''
    Embed a file from a FileField / ImageField
    '''
    fin = field.open()
    if mimetype is None:
        mimetype, _ = guess_type(field.name)
    return _embed_cid(context, fin, mimetype)


def _embed_cid(context, fobj, mimetype):
    '''
    Generates a CID URI, and stores the MIME attachment in the context.request_context
    '''
    cid = uuid4()

    if 'cid' not in context.render_context:
        context.render_context['cid'] = []

    if mimetype is None:
        mimetype = 'application/octet-stream'

    mime_main, mime_sub = mimetype.split('/', 1)

    mime_obj = MIMENonMultipart(mime_main, mime_sub, **{
        'Content-ID': '<{}>'.format(quote(str(cid)))
    })
    mime_obj.set_payload(fobj.read())

    context.render_context['cid'].append(mime_obj)

    return 'cid:{}'.format(cid)
