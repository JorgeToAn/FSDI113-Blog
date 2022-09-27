from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from posts.models import Post


class PostListView(ListView):
    template_name: str = "posts/list.html"
    model = Post


class PostDetailView(DetailView):
    template_name: str="posts/detail.html"
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name: str="posts/new.html"
    model = Post
    fields = ['title', 'author', 'subtitle', 'body']


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name: str="posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body"]

    # test_func validates the user is the author of the post to be able to manipulate it
    def test_func(self):
        post_obj = self.get_object()
        return post_obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name: str="posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post_obj = self.get_object()
        return post_obj.author == self.request.user