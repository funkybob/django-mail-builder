from django import forms

from mail_builder.views import EmailFormView


class SimpleForm(forms.Form):
    name = forms.CharField()


class SimpleView(EmailFormView):
    template_name = "form.html"
    email_template = "simple_view.email"
    form_class = SimpleForm
    success_url = "/"
