from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template import Context
from django.template.loader import select_template
from django.template.loader_tags import BlockNode


def build_message(
    template_names,
    extra_context=None,
    force_multipart=False,
    inline_images=False,
    **defaults,
):
    if not isinstance(template_names, (list, tuple)):
        template_names = (template_names,)
    template = select_template(template_names).template

    blocks = {
        node.name: node
        for node in template.nodelist.get_nodes_by_type(BlockNode)
    } # fmt: skip

    if extra_context is None:
        extra_context = {}
    context = Context(extra_context)

    data = dict(defaults)
    data.setdefault("body", "")

    # mimic Template.render()
    with context.render_context.push_state(template):
        with context.bind_template(template):
            # Scalar values
            for field in ("subject", "from_email", "body", "html"):
                block = blocks.get(field)
                if block:
                    data[field] = block.render(context).strip()

            # List values
            for field in ("to", "bcc", "cc", "reply_to"):
                block = blocks.get(field)
                if block:
                    data[field] = [
                        stripped_line
                        for line in block.render(context).splitlines()
                        if (stripped_line := line.strip())
                    ]

    html_content = data.pop("html", None)
    if force_multipart or html_content:
        msg = EmailMultiAlternatives(**data)
        if html_content:
            msg.attach_alternative(html_content, "text/html")
        if inline_images:
            for att in context.request_context.get("cid", []):
                msg.attach(att)
    else:
        msg = EmailMessage(**data)

    return msg
