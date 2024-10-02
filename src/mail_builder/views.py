import logging

from django.views.generic import FormView

from .builder import build_message

log = logging.getLogger(__name__)


class EmailFormMixin:
    """
    Mixin to send email on valid form submit.
    """

    email_template = None
    fail_silently = True
    email_kwargs = {}

    def get_email_context(self, form, **kwargs):
        kwargs.setdefault("form", form.cleaned_data)
        return kwargs

    def get_email_kwargs(self, form, **kwargs):
        kwargs.update(self.email_kwargs)
        return kwargs

    def form_valid(self, form):
        extra_context = self.get_email_context(form)
        kwargs = self.get_email_kwargs(form)

        msg = build_message(self.email_template, extra_context=extra_context, **kwargs)

        msg.send(fail_silently=self.fail_silently)

        return super().form_valid(form)


class EmailFormView(EmailFormMixin, FormView):
    """
    Convenience view.
    """
