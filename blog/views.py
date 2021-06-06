import logging

from django.shortcuts import render

from django.views import generic

from .forms import InquiryForm

from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from models import Blog

logger = logging.getLogger(__name__)

# Create your views here.

class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('blog:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)



class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_list.html'

    def get_queryset(self):
        blogs = Blog.objects.filter(user=self.request.user).order_by('-created_at')
        return blogs