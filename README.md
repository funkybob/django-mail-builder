# django-mail-builder

Build EmailMessages easily from templates

## QuickStart

In your code, you can use the ``build_message`` function to build an
``EmailMessage`` class, sourcing its values from a template.

```
def build_message(template_names, extra_context=None, force_multipart=False,
                  **defaults):
```

Parameters:

template_names::
  A list of template names to select from.  A single template name will be
  wrapped in a list.

extra_context::
  Extra context to be passed when rendering blocks from the template.

force_multipart::
  Force use of ``EmailMultipartMessage`` instead of ``EmailMessage``.

  If a `html` block is provided then ``EmailMultipartMessage`` will be used
  anyway.

defaults::
  Default values to be passed to the message class. These will be overidden by
  any template blocks.

## Template blocks

### Scalar fields:

These blocks will be rendered as is, and passed to the message. If an 'html'
block is passed, a ``EmailMultipartMessage`` will be constructed, and the
`html` content will be added as a `text/html` alternative.

- subject
- from_email
- body
- html

### List fields:

These blocks will be rendered, and then split by lines using `str.splitlines`.

- to
- bcc
- cc
- reply_to


# Views

A utility view is provided that extends ``django.views.generic.FormView`` to
send an email on form valid.

```
from mail_builder.views import EmailFormView
```

When ``form_valid`` is called, it will build a message using
``email_template``, and pass the form's cleaned_data in context as `form`. It
will then send the message using the `fail_silently` flag as set on the class.

Additional class properties:

- email_template
- email_kwargs = {}
- fail_silently = False

Two extra methods are added to allow control over context and params:

```
    def get_email_context(self, form, **kwargs):
        kwargs.setdefault('form', form.cleaned_data)
        return kwargs

    def get_email_kwargs(self, form, **kwargs):
        kwargs.update(self.email_kwargs)
        return kwargs
```


# Template Tags

Two template tags have been added to help embeding files into your emails.

To use them, add ``mail_builder`` to your `INSTALLED_APPS` setting, and include
``{% load mailbuilder %}`` in your template.


```
    <img src="{% cid_static 'static/file/name.png' %}">
    <img src="{% cid_media user.icon %}">
```

This will render the files using "cid" URIs, and place MIMEImage objects in a list in the context.


```
    msg = build_message(..., inline_images=True)
```

