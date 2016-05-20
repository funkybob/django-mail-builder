from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context
from django.template.loader import select_template
from django.template.loader_tags import BlockNode


def load_template(template_names):
    if not isinstance(template_names, (list, tuple)):
        template_names = (template_names,)
    template = select_template(template_names)
    # Unwrap for Django 1.8+
    template = getattr(template, 'template', template)

    return template

def get_blocks(template):
    return {
        node.name: node
        for node in template.nodelist.get_nodes_by_type(BlockNode)
    }


def build_message(template_names, extra_context=None, force_multipart=False,
                  **defaults):
    template = load_template(template_names)
    blocks = get_blocks(template)

    if extra_context is None:
        extra_context = {}
    extra_context = Context(extra_context)

    data = dict(defaults)
    data.setdefault('body', '')

    with extra_context.bind_template(template):
        # Scalar values
        for field in ('subject', 'from_email', 'body', 'html'):
            block = blocks.get(field)
            if block:
                data[field] = block.render(extra_context).strip()

        # List values
        for field in ('to', 'bcc', 'cc', 'reply_to'):
            block = blocks.get(field)
            if block:
                data[field] = [
                    line.strip()
                    for line in block.render(extra_context).splitlines()
                    if line.strip()
                ]

    html_content = data.pop('html', None)
    if force_multipart or html_content:
        msg = EmailMultiAlternatives(**data)
        if html_content:
            msg.attach_alternative(html_content, 'text/html')
    else:
        msg = EmailMessage(**data)

    return msg
