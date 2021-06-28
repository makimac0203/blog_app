from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('blog-list/', views.BlogListView.as_view(), name="blog_list"),
    path('blog-detail/<int:pk>/', views.BlogDetailView.as_view(), name="blog_detail"),
    path('blog-create/', views.BlogCreateView.as_view(), name="blog_create"),
    path('blog-update', views.BlogUpdateView.as_view(), name="blog_update"),
]