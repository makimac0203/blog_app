import logging

from django.shortcuts import render

from django.views import generic

from .forms import InquiryForm, BlogCreateForm

from django.urls import reverse_lazy

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Blog



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
    context_object_name = 'blogs'
    ordering = "-created_at"
    paginate_by = 2

    # def get_queryset(self):
    #     blogs = Blog.objects.filter(user=self.request.user).order_by('-created_at')
    #     return blogs


class BlogDetailView(LoginRequiredMixin, generic.DetailView):
    model = Blog
    template_name = 'blog_detail.html'
    pk_url_kwarg = 'blog_id'


class BlogCreateView(LoginRequiredMixin, generic.CreateView):
    model = Blog
    template_name = 'blog_create.html'
    form_class = BlogCreateForm
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.user = self.request.user
        blog.save()
        messages.success(self.request, '日記を作成しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の作成に失敗しました。")
        return super().form_invalid(form)


class BlogUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Blog
    template_name = 'blog_update.html'
    form_class = BlogCreateForm
    pk_url_kwarg = "blog_id"

    def get_success_url(self):
        return reverse_lazy('blog:blog_detail', kwargs={'blog_id': self.kwargs['blog_id']})

    def form_valid(self, form):
        messages.success(self.request, '日記を更新しました。')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "日記の更新に失敗しました。")
        return super().form_invalid(form)


class BlogDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Blog
    template_name = 'blog_delete.html'
    success_url = reverse_lazy('blog:blog_list')
    pk_url_kwarg = 'blog_id'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "日記を削除しました。")
        return super().delete(request, *args, **kwargs)
