from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse

from .forms import FlexibleForm
from .models import GenericModel


class FlexibleFormView(FormView):
    form_class = FlexibleForm
    template_name = 'data_saver/flexible_data_saver.html'
    model = GenericModel

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.INFO, 'form submission success',
        )
        return reverse('data_saver')

